from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import io


def index(request):
    error = None

    if request.method == "POST":

        image = request.FILES.get("image")
        target_kb = request.POST.get("target_kb")
        output_format = request.POST.get("format", "JPEG")

        # ---------- BASIC VALIDATION ----------
        if not image:
            error = "Please select an image."
            return render(request, "editor/index.html", {"error": error})

        if not target_kb:
            error = "Please enter target size in KB."
            return render(request, "editor/index.html", {"error": error})

        try:
            target_kb = int(target_kb)
            if target_kb < 10:
                raise ValueError
            target_bytes = target_kb * 1024
        except ValueError:
            error = "Enter a valid number (minimum 10 KB)."
            return render(request, "editor/index.html", {"error": error})

        # ---------- IMAGE PROCESS ----------
        try:
            img = Image.open(image)

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            buffer = io.BytesIO()
            quality = 95

            while quality > 10:
                buffer.seek(0)
                buffer.truncate(0)

                if output_format == "PNG":
                    img.save(buffer, format="PNG", optimize=True)
                else:
                    img.save(
                        buffer,
                        format="JPEG",
                        quality=quality,
                        optimize=True
                    )

                if buffer.tell() <= target_bytes:
                    break

                quality -= 5

            buffer.seek(0)

        except Exception:
            error = "Image compression failed."
            return render(request, "editor/index.html", {"error": error})

        # ---------- RESPONSE ----------
        if output_format == "PNG":
            content_type = "image/png"
            filename = f"compressed_{target_kb}kb.png"
        else:
            content_type = "image/jpeg"
            filename = f"compressed_{target_kb}kb.jpg"

        response = HttpResponse(buffer, content_type=content_type)
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    return render(request, "editor/index.html")
