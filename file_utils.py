import xlsxwriter


def save_suggestions_to_xls(suggestions, filename):
    """Save suggestions to Excel file with all metadata."""
    wb = xlsxwriter.Workbook(filename)
    ws = wb.add_worksheet()

    ws.write(0, 0, "Titre")
    ws.write(0, 1, "Catégorie")
    ws.write(0, 2, "Score IA")
    ws.write(0, 3, "Note SC Globale")
    ws.write(0, 4, "Raison")

    for i, s in enumerate(suggestions, start=1):
        ws.write(i, 0, s["title"])
        ws.write(i, 1, s["category"])
        ws.write(i, 2, s["score"])
        ws.write(i, 3, s.get("rating_sc_global"))
        ws.write(i, 4, s.get("reason", ""))

    wb.close()
