import json
from urllib import error, request


class OllamaProvider:
    def __init__(self, model="qwen2.5", base_url="http://127.0.0.1:11434", timeout=180):
        self.model = str(model or "qwen2.5").strip()
        self.base_url = str(base_url or "http://127.0.0.1:11434").rstrip("/")
        self.timeout = int(timeout or 180)

    def generar(self, prompt):
        payload = {
            "model": self.model,
            "prompt": str(prompt or ""),
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0,
            },
        }
        body = json.dumps(payload).encode("utf-8")
        req = request.Request(
            f"{self.base_url}/api/generate",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
        except error.HTTPError as exc:
            detalle = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Ollama devolvió HTTP {exc.code}: {detalle}") from exc
        except error.URLError as exc:
            raise RuntimeError(
                "No se pudo conectar con Ollama. Verifique que esta iniciado en http://127.0.0.1:11434."
            ) from exc
        except Exception as exc:
            raise RuntimeError(f"Error al invocar Ollama: {exc}") from exc

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Ollama devolvió una respuesta no válida.") from exc

        texto = str(data.get("response", "") or "").strip()
        if not texto:
            raise RuntimeError("Ollama no devolvió contenido.")
        return texto
