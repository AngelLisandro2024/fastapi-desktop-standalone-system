import sys
import os

# --- PARCHE PARA EVITAR ERROR DE UVICORN CON --noconsole ---
class DummyStream:
    def write(self, *args, **kwargs): pass
    def flush(self, *args, **kwargs): pass
    def isatty(self): return False

if sys.stdout is None:
    sys.stdout = DummyStream()
if sys.stderr is None:
    sys.stderr = DummyStream()
# ----------------------------------------------------------

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import io
import webbrowser
import threading

# ReportLab imports para la generación del PDF
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

app = FastAPI(title="Sistema Code")

# --- ABRIR EL NAVEGADOR AUTOMÁTICAMENTE AL INICIAR ---
@app.on_event("startup")
def startup_event():
    # Espera 1.2 segundos para asegurar que Uvicorn levantó el servidor antes de abrir la pestaña
    threading.Timer(1.2, lambda: webbrowser.open("http://127.0.0.1:8000")).start()

# --- CONFIGURACIÓN DE RUTAS PARA PYINSTALLER ---
def get_resource_path(relative_path):
    """ Obtiene la ruta absoluta para recursos tanto en desarrollo como en el .exe compilado """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Configuración de plantillas Jinja2 compatible con PyInstaller
templates = Jinja2Templates(directory=get_resource_path("templates"))

# Bases de datos en memoria (Simulación)
USERS_DB = [
    {"id": 1, "name": "Carlos Mendoza", "role": "Estudiante", "created_at": "2026-03-20 10:15"},
    {"id": 2, "name": "María Fernández", "role": "Estudiante", "created_at": "2026-03-21 14:30"},
    {"id": 3, "name": "Alejandro Pérez", "role": "Empleado", "created_at": "2026-03-22 09:00"}
]

INVENTORY_DB = [
    {
        "id": 1,
        "item_name": "Laptop Dell Latitude",
        "user_name": "Carlos Mendoza",
        "entry_time": "2026-03-25T08:30",
        "exit_time": "2026-03-25T14:00"
    },
    {
        "id": 2,
        "item_name": "Kit Arduino Uno R3",
        "user_name": "María Fernández",
        "entry_time": "2026-03-26T09:15",
        "exit_time": ""
    }
]

# --- RUTAS DE NAVEGACIÓN Y VISTAS HTML ---

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "users_count": len(USERS_DB),
            "inventory_count": len(INVENTORY_DB),
            "recent_inventory": INVENTORY_DB[-5:]
        }
    )

@app.get("/users", response_class=HTMLResponse)
async def list_users(request: Request):
    return templates.TemplateResponse(
        "users.html",
        {
            "request": request,
            "users": USERS_DB
        }
    )

@app.post("/users")
async def create_user(request: Request, name: str = Form(...), role: str = Form(...)):
    new_user = {
        "id": len(USERS_DB) + 1,
        "name": name,
        "role": role,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    USERS_DB.append(new_user)
    return templates.TemplateResponse(
        "users.html",
        {
            "request": request,
            "users": USERS_DB
        }
    )

@app.get("/inventory", response_class=HTMLResponse)
async def list_inventory(request: Request):
    return templates.TemplateResponse(
        "inventory.html",
        {
            "request": request,
            "inventory": INVENTORY_DB,
            "users": USERS_DB
        }
    )

@app.post("/inventory")
async def create_inventory_item(
    request: Request,
    item_name: str = Form(...),
    user_name: str = Form(...),
    entry_time: str = Form(...),
    exit_time: str = Form("")
):
    new_item = {
        "id": len(INVENTORY_DB) + 1,
        "item_name": item_name,
        "user_name": user_name,
        "entry_time": entry_time.replace("T", " "),
        "exit_time": exit_time.replace("T", " ") if exit_time else ""
    }
    INVENTORY_DB.append(new_item)
    return templates.TemplateResponse(
        "inventory.html",
        {
            "request": request,
            "inventory": INVENTORY_DB,
            "users": USERS_DB
        }
    )

# --- RUTAS DE GENERACIÓN DE REPORTE EN PDF ---

@app.get("/reports/pdf")
async def generate_pdf_report():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    story = []
    styles = getSampleStyleSheet()

    # Estilos personalizados
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=colors.HexColor('#5b21b6'),  # Purple Dark
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#2563eb'),  # Blue
        spaceAfter=15
    )
    
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        textColor=colors.HexColor('#1d4ed8'),
        spaceBefore=12,
        spaceAfter=8
    )

    cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=colors.HexColor('#1e293b')
    )

    header_cell_style = ParagraphStyle(
        'HeaderTableCell',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=colors.white
    )

    # Encabezado del documento
    story.append(Paragraph("Sistema Code - Reporte General", title_style))
    story.append(Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | Enfoque: Control de Asistencia e Inventario", subtitle_style))
    story.append(Spacer(1, 10))

    # --- Seccion 1: Usuarios / Estudiantes ---
    story.append(Paragraph("1. Usuarios y Estudiantes Registrados", section_style))
    
    users_data = [[
        Paragraph("ID", header_cell_style),
        Paragraph("Nombre Completo", header_cell_style),
        Paragraph("Rol / Tipo", header_cell_style),
        Paragraph("Fecha Registro", header_cell_style)
    ]]

    for u in USERS_DB:
        users_data.append([
            Paragraph(str(u["id"]), cell_style),
            Paragraph(u["name"], cell_style),
            Paragraph(u["role"], cell_style),
            Paragraph(u["created_at"], cell_style)
        ])

    users_table = Table(users_data, colWidths=[40, 200, 120, 180])
    users_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7c3aed')),  # Brand Purple
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(users_table)

    story.append(Spacer(1, 15))

    # --- Seccion 2: Control de Registros e Inventario ---
    story.append(Paragraph("2. Control de Inventario y Movimientos de Tiempos", section_style))

    inv_data = [[
        Paragraph("ID", header_cell_style),
        Paragraph("Item / Activo", header_cell_style),
        Paragraph("Responsable", header_cell_style),
        Paragraph("Fecha/Hora Entrada", header_cell_style),
        Paragraph("Fecha/Hora Salida", header_cell_style)
    ]]

    for item in INVENTORY_DB:
        inv_data.append([
            Paragraph(str(item["id"]), cell_style),
            Paragraph(item["item_name"], cell_style),
            Paragraph(item["user_name"], cell_style),
            Paragraph(item["entry_time"], cell_style),
            Paragraph(item["exit_time"] if item["exit_time"] else "En curso", cell_style)
        ])

    inv_table = Table(inv_data, colWidths=[30, 150, 130, 115, 115])
    inv_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),  # Brand Blue
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(inv_table)

    # Construir el PDF
    doc.build(story)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=reporte_sistema_code.pdf"}
    )

# --- PUNTO DE ENTRADA PARA EL EJECUTABLE ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)