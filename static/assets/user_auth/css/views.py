import secrets
import smtplib
from django.contrib import messages
import re
from django.shortcuts import redirect, render
from user_auth.models import CustomUserManager, CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache, cache_control
from django.core.mail import send_mail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.contrib.auth.hashers import make_password


# Create your views here.
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        phone = request.POST.get("phone")

        print(username, email, phone, email)

        # Regex patterns for validation
        pattern = r"^[a-zA-Z0-9].*"
        pattern_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        pattern_phone = r"^(?!0{10}$)\d{10}$"
        pattern_password = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"

        if not all(
            [first_name, last_name, username, password, password2, email, phone]
        ):
            messages.error(request, "Please fill all required fields")
            return render(request, "registration/register.html")

        elif not re.match(pattern, username):
            messages.error(request, "Please enter a valid username")
            return render(request, "registration/register.html")

        elif not re.match(pattern_email, email):
            messages.error(request, "Please enter a valid email")
            return render(request, "registration/register.html")

        elif not re.match(pattern_password, password):
            messages.error(request, "Password is too weak")
            return render(request, "registration/register.html")

        elif not re.match(pattern_phone, phone):
            messages.error(request, "Please enter a valid phone number")
            return render(request, "registration/register.html")

        elif password != password2:
            messages.error(request, "Passwords do not match")
            return render(request, "registration/register.html")

        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, "registration/register.html")

        elif CustomUser.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists")
            return render(request, "registration/register.html")

        else:
            message = generate_otp()
            sender_email = "qickmart12345@gmail.com"
            receiver_email = email
            password_email = "iimhlxbajrpijcko"

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password_email)
                server.sendmail(sender_email, receiver_email, message)
        except smtplib.SMTPAuthenticationError:
            messages.error(
                request,
                "Failed to send OTP email. Please check your email configuration.",
            )
            return redirect("user_register")

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            phone=phone,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        print()
        user.save()

        request.session["email"] = email
        request.session["otp"] = message
        print(message)
        messages.success(request, "OTP is sent to your email")
        return redirect("otp")

    return render(request, "registration/register.html")


def generate_otp(length=6):
    return "".join(secrets.choice("0123456789") for i in range(length))


def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if email and password:
            user = authenticate(request, email=email, password=password)

            if user is not None and user.check_password(password):
                if not user.is_superuser and user.is_active:
                    login(request, user)
                    return redirect("login")
            else:
                # Authentication failed
                messages.error(request, "Invalid email or password")
                return render(
                    request, "registration/login.html", {"invalid_credentials": True}
                )

    return render(request, "registration/login.html")


def forget(request):
    return render(request, "registration/forget.html")


def generate_otp(length=6):
    return "".join(secrets.choice("0123456789") for i in range(length))


@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def verify_otp(request):
    context = {"messages": messages.get_messages(request)}

    if request.method == "POST":
        user = CustomUser.objects.get(email=request.session["email"])
        x = request.session.get("otp")
        print(x)

        otp1 = request.POST["otp1"]
        otp2 = request.POST["otp2"]
        otp3 = request.POST["otp3"]
        otp4 = request.POST["otp4"]
        otp5 = request.POST["otp5"]
        otp6 = request.POST["otp6"]
        OTP = str(otp1) + str(otp2) + str(otp3) + str(otp4) + str(otp5) + str(otp6)

        if OTP == x:

            del request.session["email"]
            del request.session["otp"]
            messages.success(request, "Signup successful!")
            return redirect("home")
        else:
            user.delete()
            messages.info(request, "invalid otp")
            del request.session["email"]
            return redirect("login")
    return render(request, "registration/verify.html", context)


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


def cancel_view(request):

    user = CustomUser.objects.get(email=request.session["email"])
    user.delete()
    messages.info(request, "invalid otp")
    del request.session["email"]
    return redirect("login")


def forget_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            user = CustomUser.objects.filter(email=email).first()
            if user:
                # Generate OTP
                otp = generate_otp()
                print(otp)
                # Send OTP to user's email
                send_otp_email(email, otp)
                # Store OTP and email in session
                request.session["email"] = email
                request.session["otp"] = otp
                # Redirect to OTP verification page
                return redirect("otp")
            else:
                messages.error(request, "User with this email does not exist.")
        else:
            messages.error(request, "Please provide an email address.")
    return render(request, "forgot_password.html")


def send_otp_email(email, otp):
    # Email configuration
    sender_email = "qickmart12345@gmail.com"
    receiver_email = email
    password = "iimhlxbajrpijcko"
    subject = "Your OTP for password reset"
    body = f"Your OTP for password reset is: {otp}"

    # Constructing the email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        # Establishing connection with the email server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        # Logging in to the email server
        server.login(sender_email, password)

        # Sending the email
        server.sendmail(sender_email, receiver_email, msg.as_string())

        # Closing the connection
        server.quit()

        # Returning True indicating successful email sending
        return True

    except smtplib.SMTPAuthenticationError:
        # Return False if authentication fails
        return False


def verify_reset_otp(request):
    print("checking")
    if request.method == "POST":
        email = request.session.get("email")
        if email:
            user = CustomUser.objects.filter(email=email).first()
            if user:
                x = request.session.get("otp")
                print(x)  # Print the OTP

                otp1 = request.POST.get("otp1")
                otp2 = request.POST.get("otp2")
                otp3 = request.POST.get("otp3")
                otp4 = request.POST.get("otp4")
                otp5 = request.POST.get("otp5")
                otp6 = request.POST.get("otp6")
                OTP = (
                    str(otp1)
                    + str(otp2)
                    + str(otp3)
                    + str(otp4)
                    + str(otp5)
                    + str(otp6)
                )

                if OTP == x:
                    del request.session["email"]
                    del request.session["otp"]
                    # Implement your logic for resetting the password here
                    # For example, redirect to a view where the user can reset their password
                    return redirect("reset_password")
                else:
                    messages.info(request, "Invalid OTP")
            else:
                messages.error(request, "User with this email does not exist.")
        else:
            messages.error(request, "Email not found in session")
    else:
        messages.error(request, "Invalid request method")

    return redirect("reset_password")  # Redirect to login page or wherever appropriate


def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Define password pattern
        pattern_password = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"

        # Validate password against the pattern
        if not re.match(pattern_password, password):
            messages.error(
                request,
                "Password is too weak. It must contain at least one lowercase letter, one uppercase letter, one digit, and be at least 8 characters long.",
            )
            return redirect(
                "reset_password"
            )  # Redirect back to reset password page with error message

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect(
                "reset_password"
            )  # Redirect back to reset password page with error message

        user = CustomUser.objects.get(email=email)
        user.password = make_password(password)
        user.save()

        messages.success(
            request,
            "Password reset successful. You can now login with your new password.",
        )
        return redirect("login")

    return render(request, "reset_password.html")
