# Feature Specification: FailureOnTheFly

**Feature Branch**: `001-diagnostic-training-sim`
**Created**: 2026-03-09
**Status**: Draft
**Input**: User description: "Entwicklung eines webbasierten Prototyps zur Simulation von Schüler-Lehrkraft-Gesprächen. Ziel ist das Training diagnostischer Kompetenzen. Die Lehrkraft interagiert per Spracheingabe mit einem simulierten Schüler (LLM), um den Gedankengang des Schülers bei einer fehlerhaft gelösten Matheaufgabe nachzuvollziehen. Am Ende des Gesprächs gibt die Lehrkraft eine Diagnose ab."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Diagnostisches Gespräch führen (Priority: P1)

Die Webanwendung ist in drei chronologische Hauptbereiche unterteilt:

1. **Kopfbereich (Kontext)**: Eine statische Beschreibung der Unterrichtssituation (z. B. "Du gehst durch die Klasse...") und ein Bild/Text der konkret gelösten (fehlerhaften) Matheaufgabe des Schülers.
2. **Interaktionsbereich (Chat & Audio)**: Ein Mikrofon-Button ("Mikrofon halten/klicken zum Sprechen") und ein Chat-Verlauf, der die transkribierte Sprache der Lehrkraft (rechts) und die Text-Antworten des simulierten Schülers (links) dynamisch anzeigt.
3. **Abschlussbereich**: Ein Button "Ich bin jetzt so weit" (beendet den Chat und deaktiviert das Mikrofon) sowie ein Diagnose-Bereich, der erst nach Klick auf diesen Button sichtbar wird.

Die Lehrkraft nutzt den Mikrofon-Button im Interaktionsbereich, um Fragen zu stellen. Die Spracheingabe wird transkribiert und im Chat-Verlauf rechts angezeigt. Der simulierte Schüler (LLM) antwortet konsistent mit einem vordefinierten Fehlermuster; seine Antworten erscheinen links im Chat. Die Lehrkraft stellt gezielte Fragen, um den Gedankengang des Schülers Schritt für Schritt zu rekonstruieren.

**Why this priority**: Dies ist die Kernfunktionalität des Prototyps — ohne das Gespräch gibt es kein Training. Es liefert den zentralen Mehrwert für angehende Lehrkräfte.

**Independent Test**: Kann vollständig getestet werden, indem eine Lehrkraft ein Gespräch startet, Fragen per Spracheingabe stellt und prüft, ob der simulierte Schüler kohärent und fehlermuster-konsistent antwortet.

**Acceptance Scenarios**:

1. **Given** die Lehrkraft hat die Anwendung geöffnet, **When** die Seite geladen ist, **Then** sieht sie im Kopfbereich die Unterrichtssituation und die fehlerhafte Matheaufgabe, darunter den Interaktionsbereich mit Mikrofon-Button und leerem Chat-Verlauf.
2. **Given** die Lehrkraft befindet sich im Interaktionsbereich, **When** sie den Mikrofon-Button drückt und eine Frage spricht, **Then** wird die Spracheingabe transkribiert und als Lehrkraft-Nachricht rechts im Chat angezeigt.
3. **Given** die Lehrkraft hat eine Frage gestellt, **When** der simulierte Schüler antwortet, **Then** erscheint die Antwort links im Chat, konsistent mit dem vordefinierten Fehlermuster und dem bisherigen Gesprächsverlauf.
4. **Given** ein laufendes Gespräch, **When** die Lehrkraft eine Folgefrage stellt die auf vorherige Antworten Bezug nimmt, **Then** berücksichtigt der Schüler den gesamten Gesprächskontext in seiner Antwort.

---

### User Story 2 - Diagnose abgeben (Priority: P2)

Nach dem Gespräch klickt die Lehrkraft auf "Ich bin jetzt so weit". Der Chat und das Mikrofon werden deaktiviert, und im Abschlussbereich wird ein hybrider Diagnose-Bereich sichtbar. Dieser enthält:

- Ein **Single-Choice-System** mit vorgefertigten Fehlvorstellungen (z. B. "Stellenwertfehler", "Operatorverwechslung") — die Lehrkraft wählt das erkannte Fehlermuster aus.
- Ein **Freitextfeld** für eine ausführliche Beschreibung der Diagnose — die Lehrkraft erklärt in eigenen Worten, wo der Denkfehler liegt.

Die Lehrkraft gibt ihre Diagnose über beide Komponenten ab und bestätigt sie.

**Why this priority**: Die Diagnose ist das Lernziel des Trainings. Ohne Diagnoseabgabe fehlt der reflektive Abschluss, aber das Gespräch allein hat bereits Trainingswert.

**Independent Test**: Kann getestet werden, indem nach einem abgeschlossenen Gespräch der Button "Ich bin jetzt so weit" geklickt wird, der Diagnose-Bereich erscheint, eine Fehlvorstellung ausgewählt und eine Freitext-Diagnose eingegeben wird.

**Acceptance Scenarios**:

1. **Given** die Lehrkraft hat ein Gespräch geführt, **When** sie auf "Ich bin jetzt so weit" klickt, **Then** werden Chat und Mikrofon deaktiviert und der Diagnose-Bereich wird im Abschlussbereich sichtbar.
2. **Given** der Diagnose-Bereich ist sichtbar, **When** die Lehrkraft eine vorgefertigte Fehlvorstellung auswählt (Single-Choice), **Then** wird die Auswahl als Teil der Diagnose gespeichert.
3. **Given** der Diagnose-Bereich ist sichtbar, **When** die Lehrkraft eine Freitext-Diagnose eingibt, **Then** wird der Text als Teil der Diagnose gespeichert.
4. **Given** die Lehrkraft hat ihre Diagnose abgegeben, **When** die Diagnose gespeichert wurde, **Then** sieht die Lehrkraft eine Zusammenfassung des Gesprächs und ihrer Diagnose.

---

### User Story 3 - Unterrichtssituation und Aufgabe einsehen (Priority: P3)

Im Kopfbereich der Anwendung sieht die Lehrkraft dauerhaft eine Beschreibung der Unterrichtssituation (narrativer Text, z. B. "Du gehst durch die Klasse und schaust dir die Hefte an...") sowie die konkrete Matheaufgabe mit der fehlerhaften Schülerlösung als Bild oder Text. Dieser Bereich bleibt während des gesamten Gesprächs und der Diagnose sichtbar.

**Why this priority**: Der Kopfbereich liefert den Kontext für das Gespräch. Er ist statisch und kann als erstes implementiert werden, ist aber ohne den Interaktionsbereich nicht eigenständig nutzbar.

**Independent Test**: Kann getestet werden, indem geprüft wird, ob die Unterrichtssituation und die Aufgabe mit Schülerlösung im Kopfbereich korrekt dargestellt werden und während des Gesprächs sichtbar bleiben.

**Acceptance Scenarios**:

1. **Given** die Lehrkraft öffnet die Anwendung, **When** die Seite geladen ist, **Then** zeigt der Kopfbereich die Beschreibung der Unterrichtssituation und die fehlerhafte Matheaufgabe an.
2. **Given** ein laufendes Gespräch oder der Diagnose-Bereich ist aktiv, **When** die Lehrkraft nach oben scrollt, **Then** ist der Kopfbereich mit Situation und Aufgabe weiterhin sichtbar.

---

### Edge Cases

- Was passiert, wenn die Spracherkennung die Eingabe nicht versteht oder kein Audiosignal empfängt? → Fehlermeldung anzeigen, erneut versuchen lassen.
- Was passiert, wenn die Lehrkraft das Gespräch beendet, ohne eine Diagnose abzugeben? → Erlaubt, kein Zwang zur Diagnose.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST eine fehlerhaft gelöste Matheaufgabe mit Aufgabenstellung, korrekter Lösung und Schülerlösung anzeigen.
- **FR-002**: System MUST Spracheingabe über das Mikrofon des Geräts aufnehmen und in Text umwandeln (Speech-to-Text).
- **FR-003**: System MUST die transkribierte Frage zusammen mit der bisherigen Chat-Historie und einem System-Prompt an das LLM senden, das einen Schüler mit einem spezifischen Fehlermuster simuliert.
- **FR-004**: System MUST die Antwort des simulierten Schülers als strukturiertes Objekt empfangen (mit sichtbarer Antwort und optionalem internen Gedankengang) und den Antworttext im Chat anzeigen.
- **FR-005**: System MUST den gesamten Gesprächsverlauf sichtbar halten, sodass die Lehrkraft frühere Fragen und Antworten nachlesen kann.
- **FR-006**: System MUST einen Button "Ich bin jetzt so weit" anbieten, der den Chat und das Mikrofon deaktiviert und den Diagnose-Bereich im Abschlussbereich sichtbar macht.
- **FR-007**: System MUST im Diagnose-Bereich ein hybrides Formular bereitstellen: ein Single-Choice-System mit vorgefertigten Fehlvorstellungen UND ein Freitextfeld für eine ausführliche Diagnose.
- **FR-008**: System MUST die abgegebene Diagnose (gewählte Fehlvorstellung + Freitext) zusammen mit dem Gesprächsverlauf speichern.
- **FR-009**: System MUST dem simulierten Schüler ein konsistentes Fehlermuster vorgeben, das sich über das gesamte Gespräch nicht widerspricht.
- **FR-010**: System MUST die Lehrkraft darüber informieren, wenn die Spracherkennung fehlschlägt oder kein Audio empfangen wird.
- **FR-011**: System MUST Spracheingabe und Texteingabe als gleichwertige Eingabekanäle anbieten. Die Lehrkraft kann beide parallel nutzen, muss sich aber vor dem Absenden entscheiden, welchen Kanal sie abschickt (entweder die Sprachaufnahme oder den getippten Text).
- **FR-012**: System MUST die Web-Oberfläche in drei chronologische Hauptbereiche gliedern: Kopfbereich (Unterrichtssituation + Aufgabe), Interaktionsbereich (Mikrofon-Button + Chat-Verlauf), Abschlussbereich (Beenden-Button + Diagnose).
- **FR-013**: System MUST im Kopfbereich eine statische Beschreibung der Unterrichtssituation und die fehlerhafte Matheaufgabe (als Bild oder Text) anzeigen.
- **FR-014**: System MUST im Chat-Verlauf die Lehrkraft-Nachrichten rechts und die Schüler-Antworten links darstellen.
- **FR-015**: System MUST vorgefertigte Fehlvorstellungen als Single-Choice-Optionen im Diagnose-Bereich bereitstellen, die zur jeweiligen Matheaufgabe passen.
- **FR-016**: System MUST den LLM-Provider über eine Umgebungsvariable (`LLM_PROVIDER`) konfigurierbar machen (z. B. `openai`, `anthropic`), ohne den restlichen Code zu ändern.
- **FR-017**: System MUST den Chat-Verlauf pro Session vollständig speichern, sodass der simulierte Schüler sich an alle vorherigen Aussagen der Lehrkraft im selben Gespräch erinnert.

### Key Entities

- **Aufgabe (Task)**: Unterrichtssituation, Aufgabenstellung, korrekte Lösung, fehlerhafte Schülerlösung, Fehlermuster (Name + System-Prompt), Diagnose-Optionen (Label + is_correct). Alles in einem JSON-Objekt in `tasks.json`.
- **Gesprächsverlauf**: Liste von Nachrichten (`role` + `content`) in `st.session_state`. Kein separates Entity — ist die Session selbst.
- **Diagnose**: Gewählte Fehlvorstellung (Single-Choice) + Freitext. Gespeichert in `st.session_state`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Lehrkräfte können innerhalb von 30 Sekunden nach Öffnen der Anwendung ein diagnostisches Gespräch beginnen.
- **SC-002**: Der simulierte Schüler antwortet innerhalb von 5 Sekunden auf eine Frage der Lehrkraft.
- **SC-003**: Der simulierte Schüler bleibt über ein Gespräch von mindestens 15 Nachrichten hinweg konsistent im zugewiesenen Fehlermuster.
- **SC-004**: Lehrkräfte können eine Diagnose innerhalb von 2 Minuten nach Gesprächsende abgeben.

## Assumptions

- Der Prototyp wird als Einzelnutzer-Anwendung entwickelt (keine gleichzeitige Nutzung durch mehrere Lehrkräfte erforderlich).
- Es wird zunächst eine einzelne, vordefinierte Matheaufgabe mit einem festen Fehlermuster verwendet.
- Die Spracherkennung nutzt die OpenAI Whisper API; Audioaufnahme erfolgt über Streamlit-native Widgets.
- Die Anwendung wird auf Desktop-Browsern mit Mikrofon genutzt; mobile Optimierung ist nicht Teil des Prototyps.
- Die Sprache der Interaktion ist Deutsch.
- Es ist keine Benutzeranmeldung oder Authentifizierung erforderlich.
- Die Diagnose wird nicht automatisch ausgewertet oder mit einer Musterlösung verglichen — dies könnte in einer späteren Iteration ergänzt werden.
