"""
Генератор полетной документации (PDF).
"""
import io
from datetime import datetime, timezone
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from .metar_gen import generate_metar
from .taf_gen import generate_taf
from ..utils.time_utils import get_unix_timestamp


def create_brief_pdf(flight_plan, aerodromes):
    """Создаёт PDF с полетной документацией."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Поля
    left = 20 * mm
    top = height - 20 * mm
    line_height = 6 * mm

    # Заголовок
    c.setFont("Helvetica-Bold", 16)
    c.drawString(left, top, "FLIGHT DOCUMENTATION")
    c.setFont("Helvetica", 10)

    y = top - 12 * mm

    # Информация о рейсе
    c.drawString(left, y, f"Callsign: {flight_plan.callsign or 'N/A'}")
    y -= line_height
    c.drawString(left, y, f"Aircraft: {flight_plan.aircraft_type or 'N/A'}")
    y -= line_height
    if flight_plan.departure and flight_plan.destination:
        c.drawString(left, y, f"Route: {flight_plan.departure} -> {flight_plan.destination}")
        y -= line_height
    if flight_plan.cruising_level:
        c.drawString(left, y, f"Level: {flight_plan.cruising_level}")
        y -= line_height

    y -= 5 * mm

    # Аэродром вылета
    dep = aerodromes.get('departure')
    if dep:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(left, y, "DEPARTURE AERODROME")
        y -= line_height
        c.setFont("Helvetica", 10)
        c.drawString(left, y, f"{dep.icao_code} - {dep.name}")
        y -= line_height

        metar_props = generate_metar(dep)
        taf_props = generate_taf(dep)
        c.drawString(left, y, f"METAR: {metar_props['raw']}")
        y -= line_height
        c.drawString(left, y, f"TAF: {taf_props['raw']}")
        y -= line_height
        y -= 3 * mm

    # Аэродром посадки
    dest = aerodromes.get('destination')
    if dest:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(left, y, "DESTINATION AERODROME")
        y -= line_height
        c.setFont("Helvetica", 10)
        c.drawString(left, y, f"{dest.icao_code} - {dest.name}")
        y -= line_height

        metar_props = generate_metar(dest)
        taf_props = generate_taf(dest)
        c.drawString(left, y, f"METAR: {metar_props['raw']}")
        y -= line_height
        c.drawString(left, y, f"TAF: {taf_props['raw']}")
        y -= line_height
        y -= 3 * mm

    # Запасной аэродром
    alt = aerodromes.get('alternate')
    if alt:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(left, y, "ALTERNATE AERODROME")
        y -= line_height
        c.setFont("Helvetica", 10)
        c.drawString(left, y, f"{alt.icao_code} - {alt.name}")
        y -= line_height

        metar_props = generate_metar(alt)
        taf_props = generate_taf(alt)
        c.drawString(left, y, f"METAR: {metar_props['raw']}")
        y -= line_height
        c.drawString(left, y, f"TAF: {taf_props['raw']}")
        y -= line_height
        y -= 3 * mm

    # Маршрут
    route_points = flight_plan.get_route_points()
    if route_points:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(left, y, "ROUTE")
        y -= line_height
        c.setFont("Helvetica", 10)
        c.drawString(left, y, "Points: " + ", ".join(route_points))
        y -= line_height
        y -= 3 * mm

    # Разделитель
    c.line(left, y, width - left, y)
    y -= 3 * mm
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(left, y, f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    y -= line_height
    c.drawString(left, y, "Weather Server Emulator")

    c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes