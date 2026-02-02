from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import io


def index(request):
    if request.method == "POST":
        image = request.FILES.get("image")
        target_kb = request.POST.get("target_kb")
        output_format = request.POST.get("format", "JPEG")

        # ---------- BASIC VALIDATION ----------
        if not image:
            return render(request, "editor/index.html", {
                "error": "Please select an image."
            })

        if not target_kb:
            return render(request, "editor/index.html", {
                "error": "Please enter target size in KB."
            })

        try:
            target_kb = int(target_kb)
            if target_kb < 10:
                raise ValueError
            target_bytes = target_kb * 1024
        except ValueError:
            return render(request, "editor/index.html", {
                "error": "Enter a valid number (minimum 10 KB)."
            })

        # ---------- IMAGE PROCESS ----------
        try:
            img = Image.open(image)

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            buffer = io.BytesIO()

            # ---------- PNG (single pass) ----------
            if output_format == "PNG":
                buffer.seek(0)
                buffer.truncate(0)

                img.save(buffer, format="PNG", optimize=True)

                content_type = "image/png"
                filename = f"compressed_{target_kb}kb.png"

            # ---------- JPEG (quality loop) ----------
            else:
                quality = 95

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

                content_type = "image/jpeg"
                filename = f"compressed_{target_kb}kb.jpg"

            buffer.seek(0)

            # ---------- RESPONSE ----------
            response = HttpResponse(buffer, content_type=content_type)
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response

        except Exception:
            return render(request, "editor/index.html", {
                "error": "Image processing failed. Please try another image."
            })

    return render(request, "editor/index.html")


# ---------- STATIC PAGES ----------

def privacy(request):
    return render(request, "editor/privacy.html")


def about(request):
    return render(request, "editor/about.html")


def contact(request):
    return render(request, "editor/contact.html")
