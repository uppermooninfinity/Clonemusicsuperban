# -*- coding: utf-8 -*-
import ssl
import socket
import requests
from datetime import datetime
from urllib.parse import urlparse

from pyrogram import Client, filters
from pyrogram.types import Message

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

DISCLAIMER = (
    "⚠️ DISCLAIMER:\n"
    "This scan performs PASSIVE security checks only.\n"
    "Use this tool ONLY on websites you own or have permission to test.\n"
)

SMALL_CAPS = str.maketrans(
    "abcdefghijklmnopqrstuvwxyz",
    "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ"
)


def sc(text: str) -> str:
    return text.lower().translate(SMALL_CAPS)


def normalize_url(url: str) -> str:
    if not url.startswith("http"):
        return "https://" + url
    return url


def check_headers(url: str):
    result = {
        "missing_headers": [],
        "present_headers": [],
    }

    try:
        r = requests.get(url, timeout=10)
        headers = r.headers

        security_headers = [
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Strict-Transport-Security",
            "Referrer-Policy",
        ]

        for h in security_headers:
            if h in headers:
                result["present_headers"].append(h)
            else:
                result["missing_headers"].append(h)

    except Exception:
        pass

    return result


def check_ssl(domain: str):
    info = {
        "https": False,
        "tls_version": "unknown",
    }

    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(
            socket.socket(), server_hostname=domain
        ) as s:
            s.settimeout(5)
            s.connect((domain, 443))
            info["https"] = True
            info["tls_version"] = s.version()
    except Exception:
        pass

    return info


def risk_level(missing_headers: int, https: bool):
    score = missing_headers
    if not https:
        score += 3

    if score <= 2:
        return "LOW"
    elif score <= 5:
        return "MEDIUM"
    else:
        return "HIGH"


def generate_text_report(domain, headers, ssl_info, risk):
    lines = [
        sc("✦ security assessment report ✦"),
        "",
        f"• {sc('website')} : {domain}",
        f"• {sc('security level')} : {sc(risk)}",
        "",
        sc("❖ identified risks"),
    ]

    if headers["missing_headers"]:
        for h in headers["missing_headers"]:
            lines.append(f"• {sc('missing header')} : {h.lower()}")
    else:
        lines.append(f"• {sc('no critical header issues detected')}")

    if not ssl_info["https"]:
        lines.append(f"• {sc('https not enforced')}")

    lines.append("")
    lines.append(sc("❖ recommendations"))
    lines.append(f"• {sc('enable missing security headers')}")
    lines.append(f"• {sc('enforce https with hsts')}")

    lines.append("")
    lines.append(DISCLAIMER)

    return "\n".join(lines)


def generate_pdf(path, domain, headers, ssl_info, risk):
    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    def p(text):
        story.append(Paragraph(text, styles["Normal"]))
        story.append(Spacer(1, 10))

    p("<b>Security Assessment Report</b>")
    p(f"Website: {domain}")
    p(f"Security Level: {risk}")
    p(f"Scan Time: {datetime.utcnow()} UTC")

    p("<b>Identified Risks</b>")
    if headers["missing_headers"]:
        for h in headers["missing_headers"]:
            p(f"- Missing Header: {h}")
    else:
        p("No critical header issues detected.")

    if not ssl_info["https"]:
        p("HTTPS not enforced.")

    p("<b>Recommendations</b>")
    p("Enable missing security headers.")
    p("Force HTTPS and HSTS.")

    p("<b>Disclaimer</b>")
    p("This scan performs passive checks only. Use only on sites you own or are authorized to test.")

    doc.build(story)


@Client.on_message(filters.command("vlscan"))
async def vlscan_handler(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/vlscan <website>\nExample: /vlscan example.com"
        )

    raw = message.command[1]
    url = normalize_url(raw)
    domain = urlparse(url).netloc

    status = await message.reply_text("🔍 Starting passive vulnerability scan...")

    headers = check_headers(url)
    ssl_info = check_ssl(domain)
    risk = risk_level(len(headers["missing_headers"]), ssl_info["https"])

    text_report = generate_text_report(domain, headers, ssl_info, risk)

    pdf_path = f"/tmp/vlscan_{domain}.pdf"
    generate_pdf(pdf_path, domain, headers, ssl_info, risk)

    await status.delete()

    await message.reply_text(
        f"```\n{text_report}\n```",
        disable_web_page_preview=True,
    )

    await message.reply_document(
        pdf_path,
        caption="📄 Vulnerability Scan Report (PDF)",
          )
