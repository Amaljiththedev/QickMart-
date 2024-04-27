from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core import mail
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model

from user_auth.models import CustomUser


def send_otp_email(receiver_email, otp):
    sender_email = "qickmart12345@gmail.com"  # Change to your email address
    password_email = "iimhlxbajrpijcko"  # Change to your email password

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Your OTP"

    body = f"Your OTP is: {otp}"
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password_email)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return True
    except Exception as e:
        return False


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            user = CustomUser.objects.filter(email=email).first()
            if user:
                otp = get_random_string(length=6, allowed_chars="1234567890")
                message = otp
                sender_email = "qickmart12345@gmail.com"
                receiver_email = email
                password_email = "iimhlxbajrpijcko"

                try:
                    with smtplib.SMTP("smtp.gmail.com", 587) as server:
                        server.starttls()
                        server.login(sender_email, password_email)
                        server.sendmail(sender_email, receiver_email, message)
                        request.session["email"] = email
                        request.session["otp"] = otp
                        return redirect("verify_otp")
                except smtplib.SMTPAuthenticationError:
                    messages.error(
                        request,
                        "Failed to send OTP email. Please check your email configuration.",
                    )
                    return redirect("user_register")
                except Exception as e:
                    messages.error(
                        request, "Failed to send OTP. Please try again later."
                    )
            else:
                messages.error(request, "No user found with this email address.")
        else:
            messages.error(request, "Please provide an email address.")
    return render(request, "registration/forget.html")


def verify_otp(request):
    if request.method == "POST":
        otp1 = request.POST["otp1"]
        otp2 = request.POST["otp2"]
        otp3 = request.POST["otp3"]
        otp4 = request.POST["otp4"]
        otp5 = request.POST["otp5"]
        otp6 = request.POST["otp6"]
        OTP = str(otp1) + str(otp2) + str(otp3) + str(otp4) + str(otp5) + str(otp6)
        stored_otp = request.session.get("otp")
        if OTP == stored_otp:
            return redirect("change_password")
        else:
            messages.error(request, "Invalid OTP. Please try again.")
    return render(request, "registration/forgot_password_otp.html")


def change_password(request):
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        if new_password == confirm_password:
            email = request.session.get("email")
            user = CustomUser.objects.filter(email=email).first()
            if user:
                user.set_password(new_password)
                user.save()
                del request.session["email"]
                del request.session["otp"]
                messages.success(request, "Password changed successfully.")
                return redirect("home")  # Redirect to login page or any other page
            else:
                messages.error(request, "No user found with this email address.")
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, "registration/change_password.html")
