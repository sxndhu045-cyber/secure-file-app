from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from django.contrib.auth.decorators import login_required

from .models import UploadedFile

import secrets
import string
import os


def home(request):
    return render(request, "website/home.html")


@login_required
def upload_file(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")

        if uploaded_file:
            characters = string.ascii_letters + string.digits

            password = ''.join(
                secrets.choice(characters)
                for _ in range(24)
            )

            file_object = UploadedFile.objects.create(
                owner=request.user,
                file=uploaded_file,
                password=password
            )

            return render(
                request,
                "website/upload_success.html",
                {
                    "file": file_object,
                    "password": password,
                }
            )

    return render(request, "website/upload.html")


def protected_file(request, file_id):
    uploaded_file = get_object_or_404(
        UploadedFile,
        id=file_id
    )

    file_name = uploaded_file.file.name.lower()
    extension = os.path.splitext(file_name)[1]

    file_type = "other"

    if extension in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
        file_type = "image"

    elif extension == ".pdf":
        file_type = "pdf"

    elif extension in [".mp4", ".webm", ".ogg"]:
        file_type = "video"

    if request.method == "POST":
        entered_password = request.POST.get("password")

        if entered_password == uploaded_file.password:
            return render(
                request,
                "website/file_access.html",
                {
                    "file": uploaded_file,
                    "unlocked": True,
                    "file_type": file_type,
                }
            )

        return render(
            request,
            "website/file_access.html",
            {
                "file": uploaded_file,
                "error": "Incorrect password. Please try again.",
                "file_type": file_type,
            }
        )

    return render(
        request,
        "website/file_access.html",
        {
            "file": uploaded_file,
            "file_type": file_type,
        }
    )
    
def download_file(request, file_id):
    uploaded_file = get_object_or_404(
        UploadedFile,
        id=file_id
    )

    if request.method == "POST":
        entered_password = request.POST.get("password")

        if entered_password == uploaded_file.password:
            return FileResponse(
                uploaded_file.file.open("rb"),
                as_attachment=True,
                filename=uploaded_file.file.name.split("/")[-1]
            )

        return render(
            request,
            "website/file_access.html",
            {
                "file": uploaded_file,
                "error": "Incorrect password. Please try again."
            }
        )

    return render(
        request,
        "website/file_access.html",
        {
            "file": uploaded_file
        }
    )


@login_required
def dashboard(request):
    files = UploadedFile.objects.filter(
        owner=request.user
    ).order_by("-uploaded_at")

    return render(
        request,
        "website/dashboard.html",
        {
            "files": files
        }
    )