import io
import json
import wave
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

try:
    from piper import PiperVoice
    from piper.config import SynthesisConfig
except ImportError:
    PiperVoice = None
    SynthesisConfig = None

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "pt_BR-faber-medium.onnx"
VOICE = None
if PiperVoice is not None and MODEL_PATH.exists():
    try:
        VOICE = PiperVoice.load(str(MODEL_PATH))
    except Exception as exc:
        print(f"[Aviso] Não foi possível carregar o modelo Piper ({MODEL_PATH.name}): {exc}")

VOICE_NOISE_SCALE = 0.667 * (0.8 + (1.2 - 1.0) * 0.35)
VOICE_NOISE_W_SCALE = 0.8 * (0.8 + (1.2 - 1.0) * 0.45)


class TTSHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in {"/", "/painel", "/painel.html", "/index.html"}:
            panel_file = ROOT / ("painel.html" if (ROOT / "painel.html").exists() else "painel_de_controle_rob_social_usb(2).html")
            html = panel_file.read_bytes()
            self.send_response(200)
            self.send_cors_headers()
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html)))
            self.end_headers()
            self.wfile.write(html)
            return

        if self.path == "/file.html":
            html = (ROOT / "file.html").read_bytes()
            self.send_response(200)
            self.send_cors_headers()
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html)))
            self.end_headers()
            self.wfile.write(html)
            return

        self.send_json(404, {"error": "Página não encontrada."})

    def do_POST(self):
        if self.path != "/api/synthesize":
            self.send_json(404, {"error": "Rota não encontrada."})
            return

        if VOICE is None or SynthesisConfig is None:
            self.send_json(
                503,
                {"error": "Modelo Piper local (pt_BR-faber-medium.onnx) não carregado. Utilize o fallback de voz do navegador."},
            )
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except Exception:
            self.send_json(400, {"error": "JSON inválido."})
            return

        text = str(payload.get("text", "")).strip()
        if not text:
            self.send_json(400, {"error": "Informe um texto para sintetizar."})
            return

        try:
            rate = float(payload.get("rate", 1.05))
            volume = max(0.1, min(1.0, float(payload.get("volume", 1.0))))
        except (TypeError, ValueError):
            self.send_json(400, {"error": "Velocidade ou volume inválido."})
            return

        if not 0.5 <= rate <= 2.0:
            self.send_json(400, {"error": "A velocidade deve estar entre 0,5 e 2,0."})
            return

        syn_config = SynthesisConfig(
            length_scale=1.0 / rate,
            noise_scale=VOICE_NOISE_SCALE,
            noise_w_scale=VOICE_NOISE_W_SCALE,
            volume=volume,
        )

        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wav_file:
            VOICE.synthesize_wav(text, wav_file, syn_config=syn_config)

        audio = buffer.getvalue()
        self.send_response(200)
        self.send_cors_headers()
        self.send_header("Content-Type", "audio/wav")
        self.send_header("Content-Length", str(len(audio)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(audio)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 3000), TTSHandler)
    print("RoboControl Studio (Dual-ESP v3.0 + Piper) em http://127.0.0.1:3000/painel")
    server.serve_forever()
