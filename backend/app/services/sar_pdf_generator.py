import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


# Regulus AML brand colors
EMERALD = colors.HexColor("#047857")
EMERALD_LIGHT = colors.HexColor("#d1fae5")
EMERALD_DARK = colors.HexColor("#064e3b")
DARK_TEXT = colors.HexColor("#1f2937")
GRAY_TEXT = colors.HexColor("#6b7280")
LIGHT_BG = colors.HexColor("#f0fdf4")
WHITE = colors.white
BORDER_COLOR = colors.HexColor("#a7f3d0")


def _build_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        "BrandTitle",
        parent=styles["Title"],
        fontSize=22,
        textColor=EMERALD_DARK,
        fontName="Helvetica-Bold",
        alignment=TA_LEFT,
        spaceAfter=2 * mm,
    ))
    styles.add(ParagraphStyle(
        "BrandSubtitle",
        parent=styles["Normal"],
        fontSize=10,
        textColor=GRAY_TEXT,
        fontName="Helvetica",
        alignment=TA_LEFT,
        spaceAfter=6 * mm,
    ))
    styles.add(ParagraphStyle(
        "SectionHeader",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=WHITE,
        fontName="Helvetica-Bold",
        backColor=EMERALD,
        borderPadding=(6, 8, 6, 8),
        spaceBefore=6 * mm,
        spaceAfter=3 * mm,
        leftIndent=0,
    ))
    styles.add(ParagraphStyle(
        "FieldLabel",
        parent=styles["Normal"],
        fontSize=9,
        textColor=GRAY_TEXT,
        fontName="Helvetica-Bold",
        spaceBefore=1 * mm,
        spaceAfter=0.5 * mm,
    ))
    styles.add(ParagraphStyle(
        "FieldValue",
        parent=styles["Normal"],
        fontSize=10,
        textColor=DARK_TEXT,
        fontName="Helvetica",
        spaceAfter=2 * mm,
        leading=14,
    ))
    styles.add(ParagraphStyle(
        "NarrativeBody",
        parent=styles["Normal"],
        fontSize=10,
        textColor=DARK_TEXT,
        fontName="Helvetica",
        spaceAfter=3 * mm,
        leading=15,
        alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        fontSize=8,
        textColor=GRAY_TEXT,
        fontName="Helvetica",
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        "ScoreBadge",
        parent=styles["Normal"],
        fontSize=11,
        fontName="Helvetica-Bold",
        alignment=TA_CENTER,
        textColor=WHITE,
    ))
    return styles


def _score_color(score: float) -> colors.HexColor:
    if score >= 75:
        return colors.HexColor("#dc2626")  # red
    if score >= 50:
        return colors.HexColor("#f59e0b")  # amber
    if score >= 20:
        return colors.HexColor("#3b82f6")  # blue
    return colors.HexColor("#10b981")      # green


def _classification_label(score: float) -> str:
    if score >= 75:
        return "HIGH RISK"
    if score >= 50:
        return "MEDIUM RISK"
    if score >= 20:
        return "LOW RISK"
    return "FALSE POSITIVE"


def generate_sar_pdf(case, document_content: str, alert=None) -> bytes:
    """Generate a professional SAR PDF and return raw bytes."""
    buffer = io.BytesIO()
    styles = _build_styles()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
    )

    story = []

    # ── Header bar ──────────────────────────────────────────────
    header_data = [[
        Paragraph("REGULUS AML", ParagraphStyle(
            "LogoText", fontName="Helvetica-Bold", fontSize=16, textColor=WHITE,
        )),
        Paragraph("Suspicious Activity Report", ParagraphStyle(
            "HeaderRight", fontName="Helvetica", fontSize=10, textColor=EMERALD_LIGHT, alignment=TA_RIGHT,
        )),
    ]]
    header_table = Table(header_data, colWidths=[100 * mm, 74 * mm])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), EMERALD_DARK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (0, 0), 10),
        ("RIGHTPADDING", (-1, -1), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("ROUNDEDCORNERS", [4, 4, 4, 4]),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 4 * mm))

    # ── Document metadata ───────────────────────────────────────
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    meta_data = [
        ["Case ID", case.case_id, "Generated", now],
        ["Account", case.account_number, "Alert ID", case.alert_id],
        ["Status", case.case_status, "Opened", case.case_opened_date.strftime("%Y-%m-%d %H:%M") if case.case_opened_date else "—"],
    ]
    meta_table = Table(meta_data, colWidths=[28 * mm, 60 * mm, 28 * mm, 58 * mm])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), EMERALD_LIGHT),
        ("BACKGROUND", (2, 0), (2, -1), EMERALD_LIGHT),
        ("TEXTCOLOR", (0, 0), (0, -1), EMERALD_DARK),
        ("TEXTCOLOR", (2, 0), (2, -1), EMERALD_DARK),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("ROUNDEDCORNERS", [3, 3, 3, 3]),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 4 * mm))

    # ── Overall Risk Score ──────────────────────────────────────
    score = case.case_score_percentage or 0.0
    score_bg = _score_color(score)
    classification = _classification_label(score)

    score_data = [[
        Paragraph(f"Overall Risk Score: <b>{score:.1f}%</b>", ParagraphStyle(
            "ScoreLeft", fontName="Helvetica", fontSize=12, textColor=DARK_TEXT,
        )),
        Paragraph(classification, ParagraphStyle(
            "Badge", fontName="Helvetica-Bold", fontSize=11, textColor=WHITE, alignment=TA_CENTER,
        )),
    ]]
    score_table = Table(score_data, colWidths=[120 * mm, 54 * mm])
    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), LIGHT_BG),
        ("BACKGROUND", (1, 0), (1, 0), score_bg),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("ROUNDEDCORNERS", [3, 3, 3, 3]),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 4 * mm))

    # ── Agent Analysis Breakdown ────────────────────────────────
    story.append(Paragraph("Agent Analysis Breakdown", styles["SectionHeader"]))

    agents = [
        ("Behavioral Analyst", case.behavoir_agent_score, case.behavoir_agent_summary),
        ("Network Analyst", case.network_agent_score, case.network_agent_summary),
        ("Contextual Scorer", case.contextual_agent_score, case.contextual_agent_summary),
        ("Evidence Collector", case.evidence_agent_score, case.evidence_agent_summary),
        ("False Positive Optimizer", case.false_positive_agent_score, case.false_positive_agent_summary),
    ]

    agent_header = [["Agent", "Score", "Summary"]]
    agent_rows = []
    for name, a_score, a_summary in agents:
        s = a_score if a_score is not None else 0.0
        agent_rows.append([
            name,
            f"{s:.0f}",
            Paragraph(a_summary or "—", ParagraphStyle(
                "CellText", fontName="Helvetica", fontSize=8.5, textColor=DARK_TEXT, leading=11,
            )),
        ])

    agent_table = Table(agent_header + agent_rows, colWidths=[42 * mm, 18 * mm, 114 * mm])
    agent_table.setStyle(TableStyle([
        # Header row
        ("BACKGROUND", (0, 0), (-1, 0), EMERALD),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("ALIGNMENT", (1, 0), (1, -1), "CENTER"),
        # Body
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("TEXTCOLOR", (0, 1), (-1, -1), DARK_TEXT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        # Grid
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(agent_table)
    story.append(Spacer(1, 4 * mm))

    # ── Case Summary ────────────────────────────────────────────
    story.append(Paragraph("Case Summary", styles["SectionHeader"]))
    if case.case_summary:
        for para in case.case_summary.split(". "):
            text = para.strip()
            if text:
                if not text.endswith("."):
                    text += "."
                story.append(Paragraph(text, styles["NarrativeBody"]))

    # ── SAR Narrative ───────────────────────────────────────────
    story.append(Paragraph("SAR Narrative", styles["SectionHeader"]))
    if document_content:
        for para in document_content.split("\n\n"):
            text = para.strip()
            if text:
                story.append(Paragraph(text, styles["NarrativeBody"]))
    else:
        story.append(Paragraph("No SAR narrative available.", styles["NarrativeBody"]))

    # ── Footer ──────────────────────────────────────────────────
    story.append(Spacer(1, 10 * mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph(
        f"This document was generated by <b>Regulus AML</b> — AI-Powered Transaction Monitoring System &nbsp;|&nbsp; {now}",
        styles["Footer"],
    ))
    story.append(Paragraph(
        "CONFIDENTIAL — For authorized compliance personnel only.",
        ParagraphStyle("FooterBold", fontName="Helvetica-Bold", fontSize=8, textColor=EMERALD_DARK, alignment=TA_CENTER),
    ))

    doc.build(story)
    return buffer.getvalue()
