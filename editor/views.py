from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import io


def index(request):
    error = None

    if request.method == "POST":

        image = request.FILES.get("image")
        target_kb = request.POST.get("target_kb")

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

        try:
            img = Image.open(image)

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            quality = 95
            buffer = io.BytesIO()

            while quality > 10:
                buffer.seek(0)
                buffer.truncate(0)

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

        response = HttpResponse(buffer, content_type="image/jpeg")
        response["Content-Disposition"] = (
            f'attachment; filename="compressed_{target_kb}kb.jpg"'
        )
        return response

    return render(request, "editor/index.html")
