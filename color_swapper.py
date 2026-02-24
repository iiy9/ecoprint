import webview
import fitz
from PIL import Image
import os
import threading
import colorsys
from io import BytesIO

class API:
    def __init__(self):
        self.input_file = None
        self.output_dir = None
        self.window = None

    def select_input(self):
        result = self.window.create_file_dialog(1, file_types=('PDF files (*.pdf)',))
        if result:
            self.input_file = result[0]
            self.window.evaluate_js(f"updateFileName('{os.path.basename(self.input_file)}')")
            self.output_dir = os.path.dirname(self.input_file)

    def run_process(self, hue):
        if not self.input_file:
            self.window.evaluate_js("onError('NO FILE')")
            return
        threading.Thread(target=self._core_logic, args=(hue,), daemon=True).start()

    def _core_logic(self, hue):
        try:
            doc = fitz.open(self.input_file)
            out = fitz.open()
            total = len(doc)

            for i, page in enumerate(doc):
                pct = int((i / total) * 100)
                self.window.evaluate_js(f"updateProgress({pct}, 'PAGE {i+1}/{total}')")
                
                pix = page.get_pixmap(dpi=150)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                pixels = img.load()
                
                for y in range(img.size[1]):
                    for x in range(img.size[0]):
                        r, g, b = pixels[x, y]
                        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
                        if l >= 0.22 and s >= 0.15: 
                            nr, ng, nb = colorsys.hls_to_rgb(hue, l, s)
                            pixels[x, y] = (int(nr*255), int(ng*255), int(nb*255))

                new_page = out.new_page(width=page.rect.width, height=page.rect.height)
                buf = BytesIO()
                img.save(buf, format='JPEG', quality=80)
                new_page.insert_image(page.rect, stream=buf.getvalue())

                text_data = page.get_text("dict")
                for blk in text_data["blocks"]:
                    if blk["type"] == 0:
                        for line in blk["lines"]:
                            for span in line["spans"]:
                                new_page.insert_text(span["origin"], span["text"], fontsize=span["size"], fontname="helv", fill_opacity=0)

            final_name = "ecoprint_" + os.path.basename(self.input_file)
            final_path = os.path.join(self.output_dir, final_name)
            out.save(final_path, garbage=4, deflate=True)
            self.window.evaluate_js(f"onComplete('COMPLETED: {final_name}')")
        except Exception as e:
            self.window.evaluate_js(f"onError('{str(e)}')")

if __name__ == '__main__':
    ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui', 'index.html')
    api = API()
    win = webview.create_window(
        'EcoPrint', 
        url=ui_path,
        width=400, 
        height=540, 
        resizable=False, 
        js_api=api
    )
    api.window = win
    webview.start()
