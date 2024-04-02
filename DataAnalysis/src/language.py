
# Dictionary containing all labels for each diagram in both languages
labels_dict = {
    1: {  # Diagram number 1
        "title": {"german": "Häufigkeitsverteilung der Zimmergröße", "english": "Frequency Distribution of Room Size"},
        "x_label": {"german": "Zimmergröße (m²)", "english": "Room Size (m²)"},
        "y_label": {"german": "Häufigkeit", "english": "Frequency"}
    },
    2: {  # Diagram number 2
        "title": {"german": "Häufigkeitsverteilung der Miete", "english": "Frequency Distribution of Rent"},
        "x_label": {"german": "Miete (€)", "english": "Rent (€)"},
        "y_label": {"german": "Häufigkeit", "english": "Frequency"}
    },
    # Add more diagram numbers and labels as needed
}

def get_labels(diagram_number, language):
    """
    Returns the labels for a specific diagram and language.

    Parameters:
    - diagram_number: The number of the diagram.
    - language: The selected language ("german" or "english").
    
    Returns:
    - A dictionary with the title, x_label, and y_label for the specified diagram and language.
    """

    diagram_labels = labels_dict.get(diagram_number, {})

    return {
        "title": diagram_labels.get("title", {}).get(language, ""),
        "x_label": diagram_labels.get("x_label", {}).get(language, ""),
        "y_label": diagram_labels.get("y_label", {}).get(language, "")
    }


