# -*- coding: utf-8 -*-
"""
Script per generare il documento PDF riepilogativo di logistica, preventivi e contatti
da allegare alla mail per la Direzione SSAS e la Segreteria.
Predisposto a cura del Comitato Organizzatore Studenti SSAS Sapienza.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)

def create_pdf(filename="preventivo_logistica_relatori_ssas.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#64748B'),
        alignment=1, # Center
        spaceAfter=10
    )
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontSize=17,
        leading=21,
        textColor=colors.HexColor('#0F172A'),
        alignment=1,
        fontName='Helvetica-Bold',
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Normal'],
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#334155'),
        alignment=1,
        fontName='Helvetica-Oblique',
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'H1Style',
        parent=styles['Heading1'],
        fontSize=12.5,
        leading=15,
        textColor=colors.HexColor('#1E3A8A'),
        fontName='Helvetica-Bold',
        spaceBefore=12,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1E293B')
    )
    
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    table_cell = ParagraphStyle(
        'TableCell',
        parent=body_style,
        fontSize=8.5,
        leading=11.5
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold'
    )
    
    table_header = ParagraphStyle(
        'TableHeader',
        parent=table_cell,
        fontName='Helvetica-Bold',
        textColor=colors.white
    )

    story = []
    
    # Intestazione istituzionale
    story.append(Paragraph("SCUOLA SUPERIORE DI STUDI AVANZATI SAPIENZA (SSAS) • COMITATO ORGANIZZATORE", header_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceBefore=2, spaceAfter=10))
    
    # Titolo
    story.append(Paragraph("DOCUMENTO RIEPILOGATIVO LOGISTICA, CONTATTI E PREVENTIVI", title_style))
    story.append(Paragraph("Conferenza sulle Nanotecnologie, Scienza dei Materiali e Ingegneria (NANOCONVERGENCE)<br/>17 - 18 Settembre 2026 • Aula Amaldi, Città Universitaria Sapienza", subtitle_style))
    story.append(Spacer(1, 8))
    
    # Sezione 1: Premessa e Obiettivo (Quadro Strettamente Necessario)
    story.append(Paragraph("1. Contatti e Quadro Logistico dei Relatori Plenari Confermati (Quadro Strettamente Necessario)", h1_style))
    story.append(Paragraph(
        "Il presente documento è stato predisposto al fine di offrire al Direttore, alle Fellows, ai Fellows e alla Segreteria della SSAS un quadro trasparente "
        "e immediato delle necessità organizzative, dei contatti e dei costi stimati per l'accoglienza dei relatori confermati.<br/>"
        "<b>Si evidenzia che il quadro logistico illustrato in questa prima sezione rappresenta esclusivamente le spese di base strettamente necessarie</b> "
        "(copertura dei soli viaggi e dei pernottamenti minimi indispensabili per lo svolgimento delle relazioni). Nelle sezioni successive del documento verranno invece "
        "presentate le ulteriori opzioni e possibilità di arricchimento dell'evento (come l'estensione del pernottamento a 2 notti per tutti i relatori e l'invito di "
        "speaker supplementari).",
        body_style
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Per garantire standard di accoglienza elevati e congrui con il prestigio dell'istituzione, le stime di costo sono state elaborate prendendo come riferimento "
        "<b>hotel 4 stelle in zona Sapienza</b> e tariffe verificate delle <b>principali compagnie aeree di linea (top tier)</b> e dell'Alta Velocità ferroviaria. "
        "Inoltre, al fine di disporre di un ragionevole margine di sicurezza sulle fluttuazioni di prezzo, si è applicato un "
        "<b>margine prudenziale di 20-30 € in più su ciascuna voce di spesa</b> (voli, treni e pernottamenti).",
        body_style
    ))
    story.append(Spacer(1, 10))
    
    # Tabella Relatori Confermati
    headers = [
        Paragraph("Relatore, Afferenza e Email", table_header),
        Paragraph("Mezzo e Tratta", table_header),
        Paragraph("Pernottamento (Base Necessaria)", table_header),
        Paragraph("Stima Costo (€)", table_header)
    ]
    
    data = [headers,
        [
            Paragraph("<b> Carlo Beenakker</b><br/>Leiden University (Paesi Bassi)<br/><i>beenakker@lorentz.leidenuniv.nl</i>", table_cell),
            Paragraph("Volo A/R<br/>Amsterdam Schiphol ↔ Roma FCO", table_cell),
            Paragraph("1 Notte (17 sett.)<br/>Hotel in zona Sapienza", table_cell),
            Paragraph("Volo: ~250-320 €<br/>Hotel: ~160-185 €<br/><b>Tot: ~410-505 €</b>", table_cell)
        ],
        [
            Paragraph("<b> Kazu Suenaga</b><br/>Osaka University / AIST (Giappone)<br/><i>suenaga@sanken.osaka-u.ac.jp</i>", table_cell),
            Paragraph("Già in Italia per conferenza<br/><i>(Nessun volo richiesto)</i>", table_cell),
            Paragraph("1 Notte (17 sett.)<br/>Hotel in zona Sapienza", table_cell),
            Paragraph("Volo: 0 €<br/>Hotel: ~160-185 €<br/><b>Tot: ~160-185 €</b>", table_cell)
        ],
        [
            Paragraph("<b> Maximilian Haider</b><br/>CEOS GmbH / KIT (Germania)<br/><i>haider@ceos-gmbh.de</i>", table_cell),
            Paragraph("Già in Italia per conferenza<br/><i>(Nessun volo richiesto)</i>", table_cell),
            Paragraph("1 Notte (17 sett.)<br/>Hotel in zona Sapienza", table_cell),
            Paragraph("Volo: 0 €<br/>Hotel: ~160-185 €<br/><b>Tot: ~160-185 €</b>", table_cell)
        ],
        [
            Paragraph("<b> Francesco De Angelis</b><br/>Istituto Italiano di Tecnologia (IIT)<br/><i>francesco.deangelis@iit.it</i>", table_cell),
            Paragraph("Volo A/R<br/><b>Da Sicilia (Palermo/Catania)</b> ↔ FCO<br/><i>(Non da Genova sede abituale)</i>", table_cell),
            Paragraph("Non necessita di pernottamento<br/><i>(Dispone di alloggio/casa a Roma)</i>", table_cell),
            Paragraph("Volo A/R: ~120-170 €<br/>Hotel: 0 €<br/><b>Tot: ~120-170 €</b>", table_cell)
        ],
        [
            Paragraph("<b> Gabriella Di Carlo</b><br/>CNR-ISMN, Roma<br/><i>gabriella.dicarlo@cnr.it</i>", table_cell),
            Paragraph("Sede di ricerca a Roma<br/><i>(Nessun viaggio richiesto)</i>", table_cell),
            Paragraph("Non necessita di pernottamento<br/><i>(Sede lavorativa/residenza a Roma)</i>", table_cell),
            Paragraph("Viaggio: 0 €<br/>Hotel: 0 €<br/><b>Tot: 0 €</b>", table_cell)
        ],
        [
            Paragraph("<b> Camilla Coletti</b><br/>IIT & CNI@NEST, Pisa<br/><i>camilla.coletti@iit.it</i>", table_cell),
            Paragraph("Treno Alta Velocità A/R<br/>Pisa Centrale ↔ Roma Termini", table_cell),
            Paragraph("Nessun pernottamento<br/><i>(Rientro in giornata)</i>", table_cell),
            Paragraph("Treno: ~80-100 €<br/>Hotel: 0 €<br/><b>Tot: ~80-100 €</b>", table_cell)
        ],
        [
            Paragraph("<b> Giulia Serrano</b><br/>Università di Firenze<br/><i>giulia.serrano@unifi.it</i>", table_cell),
            Paragraph("Treno Alta Velocità A/R<br/>Firenze S.M.N. ↔ Roma Termini", table_cell),
            Paragraph("Nessun pernottamento<br/><i>(Rientro in giornata)</i>", table_cell),
            Paragraph("Treno: ~70-90 €<br/>Hotel: 0 €<br/><b>Tot: ~70-90 €</b>", table_cell)
        ],
        [
            Paragraph("<b> Alessandro Tredicucci</b><br/>Univ. Pisa / NEST - CNR-NANO<br/><i>alessandro.tredicucci@unipi.it</i>", table_cell),
            Paragraph("Treno Alta Velocità A/R<br/>Pisa Centrale ↔ Roma Termini", table_cell),
            Paragraph("Nessun pernottamento<br/><i>(Rientro in giornata)</i>", table_cell),
            Paragraph("Treno: ~80-100 €<br/>Hotel: 0 €<br/><b>Tot: ~80-100 €</b>", table_cell)
        ],
        [
            Paragraph("<b>TOTALE RELATORI CONFERMATI (8)</b>", table_cell_bold),
            Paragraph("2 Voli + 4 Treni AV (con margine)", table_cell_bold),
            Paragraph("3 Notti Hotel tot. (Quadro Strettamente Necessario)", table_cell_bold),
            Paragraph("<b>~ 1.080 € - 1.335 €</b>", table_cell_bold)
        ]
    ]
    
    t = Table(data, colWidths=[5.4*cm, 4.6*cm, 4.2*cm, 3.8*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#F8FAFC')]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    
    story.append(t)
    story.append(Spacer(1, 12))
    
    # Sezione 2: Opzioni per 2 Relatori Plenari Supplementari (In Valutazione)
    story.append(Paragraph("2. Opzioni per 2 Relatori Plenari Supplementari (In Fase di Valutazione Budget)", h1_style))
    story.append(Paragraph(
        "Al fine di completare e arricchire ulteriormente il palinsesto scientifico, sono stati individuati <b>2 possibili relatori supplementari</b> di grande rilievo. "
        "Tuttavia, prima di procedere al contatto formale e al contestuale invito, si ritiene opportuno un confronto preventivo con la Direzione e la Segreteria per verificare "
        "l'effettiva capienza del budget residuo. A tal proposito sono state delineate due opzioni di spesa alternative fra cui operare la scelta più congrua:",
        body_style
    ))
    story.append(Spacer(1, 6))
    
    headers_extra = [
        Paragraph("Opzione Supplementare", table_header),
        Paragraph("Modalità Logistica e Tratta", table_header),
        Paragraph("Impatto sul Budget (2 Relatori inclusi)", table_header)
    ]
    data_extra = [
        headers_extra,
        [
            Paragraph("<b>Opzione A: Low Budget</b><br/>(2 Relatori da Università Italiane)", table_cell),
            Paragraph("Solo treno Alta Velocità A/R (es. Milano / Bologna / Napoli).<br/>Nessun pernottamento richiesto (rientro in giornata).", table_cell),
            Paragraph("Treni 2 pax: ~160 - 200 €<br/>Hotel: 0 €<br/><b>Totale Extra: ~160 - 200 €</b>", table_cell)
        ],
        [
            Paragraph("<b>Opzione B: International</b><br/>(2 Relatori da Università Estere/Europee)", table_cell),
            Paragraph("Volo aereo A/R per Roma FCO + pernottamento di 1 notte in hotel per ciascun relatore.", table_cell),
            Paragraph("Voli 2 pax: ~500 - 640 €<br/>Hotel (2 notti tot.): ~320 - 370 €<br/><b>Totale Extra: ~820 - 1.010 €</b>", table_cell)
        ]
    ]
    t_extra = Table(data_extra, colWidths=[5.6*cm, 7.8*cm, 4.6*cm])
    t_extra.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#334155')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_extra)
    story.append(Spacer(1, 12))
    
    # Sezione 3: Logistica Trasporti e Spazi Aule per Workshop Hands-on
    story.append(Paragraph("3. Logistica dei Trasporti e Spazi Aule per i Workshop Hands-on", h1_style))
    story.append(Paragraph(
        "Nel pomeriggio di venerdì 18 Settembre 2026 (ore 15:00 - 18:00), le sessioni pratiche parallele di laboratorio (Workshop Hands-on) "
        "richiederanno una gestione organizzativa e di spazi coordinata fra la Città Universitaria e i dipartimenti esterni:",
        body_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "• <b>Servizio Navetta / Minibus Riservato:</b> Per le attività di Ingegneria e Nanotecnologie che si svolgeranno presso la sede di "
        "<b>San Pietro in Vincoli (Via Eudossiana)</b>, è stato preventivato l'allestimento di un servizio navetta riservato SSAS con partenza dall'Aula Amaldi "
        "e rientro coordinato al termine dei workshop (stima costo prudenziale comprensiva di margine: <b>~170 - 250 €</b>).",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Utilizzo Aule Didattiche della Scuola:</b> Si segnala inoltre che per lo svolgimento di alcuni workshop pratici potrebbero risultare utili "
        "le aule didattiche della Scuola. Maggiori dettagli e richieste specifiche di prenotazione verranno comunicati non appena completate le verifiche "
        "sul numero esatto di sessioni che avranno necessità di usufruire di spazi al di fuori dei rispettivi dipartimenti di ricerca.",
        bullet_style
    ))
    story.append(Spacer(1, 12))
    
    # Sezione 4: Spese Tipografiche, Materiale Promozionale e Ristorazione (Coffee & Lunch Break)
    story.append(Paragraph("4. Spese Tipografiche, Materiali Organizzativi e Servizi di Catering", h1_style))
    story.append(Paragraph(
        "Oltre all'accoglienza e ai viaggi dei relatori, il budget complessivo dovrà tenere conto delle spese organizzative di supporto visivo, "
        "tipografico e della ristorazione per delegati e relatori durante le due giornate:",
        body_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "• <b>Materiale Tipografico e Allestimento (Posters, Banners, Badges e Locandine):</b> Sarà necessario prevedere una copertura per la stampa di "
        "locandine promozionali e flyer da distribuire nelle facoltà, roll-up e banners da posizionare nell'atrio dell'Aula Amaldi, stampa dei poster scientifici "
        "per la sessione poster dei giovani ricercatori e realizzazione dei badge/pass di accreditamento (stima complessiva: <b>~250 - 400 €</b>).",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Servizio di Catering (Coffee Breaks & Lunch Break):</b> Per garantire un'ospitalità all'altezza dell'evento, sono previsti buffet per i coffee break "
        "di mattina e pomeriggio per entrambe le giornate. Per quanto concerne invece il <b>Lunch Break (pranzo a buffet)</b>, la scelta operativa dipenderà dalla "
        "disponibilità finanziaria residua:",
        bullet_style
    ))
    story.append(Paragraph(
        "  - <i>Opzione Lunch Ristretto (Budget Limitato):</i> Pranzo a buffet riservato esclusivamente ai relatori plenari, ai membri del comitato scientifico, "
        "agli organizzatori e allo staff di supporto.<br/>"
        "  - <i>Opzione Lunch Completo (Fondi Disponibili):</i> Pranzo a buffet esteso a <b>tutti i delegati e studenti registrati</b> alla conferenza.",
        ParagraphStyle('SubBullet', parent=bullet_style, leftIndent=30, fontSize=8.5, leading=12)
    ))
    story.append(Spacer(1, 12))
    
    # Sezione 5: Riepilogo Budget Consuntivabile
    story.append(Paragraph("5. Sintesi e Scenari del Preventivo Generale (Opzioni 1 Notte vs 2 Notti)", h1_style))
    story.append(Paragraph(
        "Per consentire alla Direzione e alla Segreteria di valutare le diverse possibilità, si presentano gli scenari riepilogativi confrontando il "
        "quadro strettamente necessario (Scenario 1) con l'opzione di fornire a tutti 2 notti garantite.<br/>"
        "<b>Nota importante sui pernottamenti:</b> si specifica che sia nel caso base che nell'ipotesi in cui si offrano 2 notti a tutti i relatori plenari, "
        "il <b> Francesco De Angelis e la  Gabriella Di Carlo non necessitano di pernottamento alberghiero</b> in quanto dispongono già di "
        "abitazione o sede lavorativa a Roma. Di conseguenza, l'opzione 2 notti per tutti copre esattamente i rimanenti 6 relatori (Beenakker, Suenaga, Haider, "
        "Coletti, Serrano, Tredicucci per 2 notti ciascuno, ossia 12 notti totali invece delle 3 notti del quadro base).",
        body_style
    ))
    story.append(Spacer(1, 6))
    
    summary_headers = [
        Paragraph("Scenario e Modalità Pernottamenti", table_header),
        Paragraph("Voci Logistiche Incluse (con margini prudenziali +20-30€)", table_header),
        Paragraph("Stima Costo (€)", table_header)
    ]
    summary_data = [
        summary_headers,
        [
            Paragraph("<b>Scenario 1: Base (Strettamente Necessario)</b><br/>(8 Relatori Plenari Confermati)", table_cell),
            Paragraph("Voli/treni per tutti gli 8 confermati + 3 notti Hotel tot. (Beenakker 1n, Suenaga 1n, Haider 1n; De Angelis e Di Carlo 0n) + Navetta SPV + Spese Tipografiche base.", table_cell),
            Paragraph("<b>~ 1.500 € - 1.985 €</b>", table_cell_bold)
        ],
        [
            Paragraph("<b>Scenario 2: Full Conference (2 Notti)</b><br/>(8 Relatori Plenari Confermati)", table_cell),
            Paragraph("Voli/treni per gli 8 confermati + <b>2 notti in Hotel garantite ai 6 relatori che ne necessitano</b> (Beenakker, Suenaga, Haider, Coletti, Serrano, Tredicucci; De Angelis e Di Carlo 0n) per 12 notti tot. + Navetta SPV + Spese Tipografiche/Catering.", table_cell),
            Paragraph("<b>~ 2.550 € - 3.250 €</b>", table_cell_bold)
        ],
        [
            Paragraph("<b>Scenario 3: 2 Notti + 2 Relatori Extra (Low Budget Italia)</b>", table_cell),
            Paragraph("Scenario 2 (2 notti ai relatori confermati) + 2 Relatori supplementari italiani (treno AV + 2 notti hotel pure per loro) + Spese Tipografiche/Catering.", table_cell),
            Paragraph("<b>~ 3.030 € - 3.820 €</b>", table_cell_bold)
        ],
        [
            Paragraph("<b>Scenario 4: 2 Notti + 2 Relatori Extra (International Estero)</b>", table_cell),
            Paragraph("Scenario 2 (2 notti ai relatori confermati) + 2 Relatori supplementari esteri (voli A/R + 2 notti hotel pure per loro) + Spese Tipografiche/Catering.", table_cell),
            Paragraph("<b>~ 3.690 € - 4.630 €</b>", table_cell_bold)
        ]
    ]
    
    t_summary = Table(summary_data, colWidths=[5.4*cm, 8.0*cm, 4.6*cm])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(t_summary)
    story.append(Spacer(1, 14))
    
    doc.build(story)
    print(f"PDF generato con successo: {os.path.abspath(filename)}")

if __name__ == "__main__":
    create_pdf()
