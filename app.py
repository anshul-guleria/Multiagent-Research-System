from flask import Flask, render_template, request, jsonify, send_file
from graph.builder import build_graph
from fpdf import FPDF
import io, re

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/research", methods=["POST"])
def research():
    topic = request.json.get("topic", "").strip()
    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    graph = build_graph()
    result = graph.invoke({"topic": topic})

    return jsonify({
        "report": result.get("report", ""),
        "feedback": result.get("feedback", "")
    })

def strip_markdown(text):
    text = re.sub(r'#{1,6}\s*', '', text)          # headings
    text = re.sub(r'\*{1,3}(.+?)\*{1,3}', r'\1', text)  # bold/italic
    text = re.sub(r'`{1,3}[^`]*`{1,3}', '', text)  # code
    text = re.sub(r'^[-*+]\s+', '- ', text, flags=re.MULTILINE)  # bullets
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # links
    text = re.sub(r'-{2,}', '', text)               # horizontal rules
    return text.strip()

def safe_text(text):
    return text.encode('latin-1', errors='replace').decode('latin-1')

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    topic = safe_text(data.get("topic", "Research Report"))
    report = safe_text(strip_markdown(data.get("report", "")))
    feedback = safe_text(strip_markdown(data.get("feedback", "")))

    pdf = FPDF()
    pdf.set_margins(20, 20, 20)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, f"Research Report", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, f"Topic: {topic}", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Report", ln=True)
    pdf.ln(2)
    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(0, 6, report)
    pdf.ln(6)

    pdf.set_draw_color(200, 200, 200)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Critic Feedback", ln=True)
    pdf.ln(2)
    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(0, 6, feedback)

    pdf_str = pdf.output("", "S")
    buf = io.BytesIO(pdf_str.encode("latin-1"))
    buf.seek(0)
    return send_file(buf, mimetype="application/pdf",
                     as_attachment=True, download_name="research_report.pdf")

if __name__ == "__main__":
    app.run(debug=True)
