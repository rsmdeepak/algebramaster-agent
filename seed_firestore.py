#!/usr/bin/env python3
"""Seed script for AlgebraMaster 8th Grade Math Agent Firestore database.

Includes 8th Grade Algebra 1 Curriculum Chapters 1-11 and sample topic lessons.
"""

import subprocess
from google.cloud import firestore
from google.oauth2.credentials import Credentials

PROJECT_ID = "qwiklabs-gcp-02-7e80680db9e2"

CHAPTERS_DATA = [
    {
        "chapter_num": 1,
        "title": "Solving Linear Equations",
        "page_start": 1,
        "page_end": 56,
        "sections": [
            {"section_id": "1.1", "title": "Solving Simple Equations", "page": 3},
            {"section_id": "1.2", "title": "Solving Multi-Step Equations", "page": 11},
            {"section_id": "1.3", "title": "Modeling Quantities", "page": 19},
            {"section_id": "1.4", "title": "Accuracy with Measurements", "page": 25},
            {"section_id": "1.5", "title": "Solving Equations with Variables on Both Sides", "page": 31},
            {"section_id": "1.6", "title": "Solving Absolute Value Equations", "page": 37},
            {"section_id": "1.7", "title": "Rewriting Equations and Formulas", "page": 45},
            {"section_id": "1.R", "title": "Chapter Review", "page": 53},
            {"section_id": "1.T", "title": "Practice Test", "page": 56},
        ],
    },
    {
        "chapter_num": 2,
        "title": "Solving Linear Inequalities",
        "page_start": 63,
        "page_end": 104,
        "sections": [
            {"section_id": "2.1", "title": "Writing and Graphing Inequalities", "page": 63},
            {"section_id": "2.2", "title": "Solving Inequalities Using Addition or Subtraction", "page": 71},
            {"section_id": "2.3", "title": "Solving Inequalities Using Multiplication or Division", "page": 77},
            {"section_id": "2.4", "title": "Solving Multi-Step Inequalities", "page": 83},
            {"section_id": "2.5", "title": "Solving Compound Inequalities", "page": 89},
            {"section_id": "2.6", "title": "Solving Absolute Value Inequalities", "page": 95},
            {"section_id": "2.R", "title": "Chapter Review", "page": 101},
            {"section_id": "2.T", "title": "Practice Test", "page": 104},
        ],
    },
    {
        "chapter_num": 3,
        "title": "Graphing Linear Functions",
        "page_start": 111,
        "page_end": 180,
        "sections": [
            {"section_id": "3.1", "title": "Functions", "page": 111},
            {"section_id": "3.2", "title": "Characteristics of Functions", "page": 119},
            {"section_id": "3.3", "title": "Linear Functions", "page": 125},
            {"section_id": "3.4", "title": "Function Notation", "page": 135},
            {"section_id": "3.5", "title": "Graphing Linear Equations in Standard Form", "page": 141},
            {"section_id": "3.6", "title": "Graphing Linear Equations in Slope-Intercept Form", "page": 147},
            {"section_id": "3.7", "title": "Transformations of Linear Functions", "page": 157},
            {"section_id": "3.8", "title": "Graphing Absolute Value Functions", "page": 167},
            {"section_id": "3.R", "title": "Chapter Review", "page": 175},
            {"section_id": "3.T", "title": "Practice Test", "page": 180},
        ],
    },
    {
        "chapter_num": 4,
        "title": "Writing Linear Functions",
        "page_start": 187,
        "page_end": 238,
        "sections": [
            {"section_id": "4.1", "title": "Writing Equations in Slope-Intercept Form", "page": 187},
            {"section_id": "4.2", "title": "Writing Equations in Point-Slope Form", "page": 193},
            {"section_id": "4.3", "title": "Writing Equations of Parallel and Perpendicular Lines", "page": 199},
            {"section_id": "4.4", "title": "Scatter Plots and Lines of Fit", "page": 205},
            {"section_id": "4.5", "title": "Analyzing Lines of Fit", "page": 211},
            {"section_id": "4.6", "title": "Arithmetic Sequences", "page": 219},
            {"section_id": "4.7", "title": "Piecewise Functions", "page": 227},
            {"section_id": "4.R", "title": "Chapter Review", "page": 235},
            {"section_id": "4.T", "title": "Practice Test", "page": 238},
        ],
    },
    {
        "chapter_num": 5,
        "title": "Solving Systems of Linear Equations",
        "page_start": 245,
        "page_end": 292,
        "sections": [
            {"section_id": "5.1", "title": "Solving Systems of Linear Equations by Graphing", "page": 245},
            {"section_id": "5.2", "title": "Solving Systems of Linear Equations by Substitution", "page": 251},
            {"section_id": "5.3", "title": "Solving Systems of Linear Equations by Elimination", "page": 257},
            {"section_id": "5.4", "title": "Solving Special Systems of Linear Equations", "page": 263},
            {"section_id": "5.5", "title": "Solving Equations by Graphing", "page": 269},
            {"section_id": "5.6", "title": "Graphing Linear Inequalities in Two Variables", "page": 275},
            {"section_id": "5.7", "title": "Systems of Linear Inequalities", "page": 281},
            {"section_id": "5.R", "title": "Chapter Review", "page": 289},
            {"section_id": "5.T", "title": "Practice Test", "page": 292},
        ],
    },
    {
        "chapter_num": 6,
        "title": "Exponential Functions and Sequences",
        "page_start": 299,
        "page_end": 356,
        "sections": [
            {"section_id": "6.1", "title": "Properties of Exponents", "page": 299},
            {"section_id": "6.2", "title": "Radicals and Rational Exponents", "page": 307},
            {"section_id": "6.3", "title": "Exponential Functions", "page": 313},
            {"section_id": "6.4", "title": "Exponential Growth and Decay", "page": 321},
            {"section_id": "6.5", "title": "Solving Exponential Equations", "page": 331},
            {"section_id": "6.6", "title": "Geometric Sequences", "page": 337},
            {"section_id": "6.7", "title": "Recursively Defined Sequences", "page": 345},
            {"section_id": "6.R", "title": "Chapter Review", "page": 353},
            {"section_id": "6.T", "title": "Practice Test", "page": 356},
        ],
    },
    {
        "chapter_num": 7,
        "title": "Polynomial Equations and Factoring",
        "page_start": 363,
        "page_end": 418,
        "sections": [
            {"section_id": "7.1", "title": "Adding and Subtracting Polynomials", "page": 363},
            {"section_id": "7.2", "title": "Multiplying and Dividing Polynomials", "page": 371},
            {"section_id": "7.3", "title": "Special Products of Polynomials", "page": 379},
            {"section_id": "7.4", "title": "Solving Polynomial Equations in Factored Form", "page": 385},
            {"section_id": "7.5", "title": "Factoring x^2 + bx + c", "page": 391},
            {"section_id": "7.6", "title": "Factoring ax^2 + bx + c", "page": 397},
            {"section_id": "7.7", "title": "Factoring Special Products", "page": 403},
            {"section_id": "7.8", "title": "Factoring Polynomials Completely", "page": 409},
            {"section_id": "7.R", "title": "Chapter Review", "page": 415},
            {"section_id": "7.T", "title": "Practice Test", "page": 418},
        ],
    },
    {
        "chapter_num": 8,
        "title": "Graphing Quadratic Functions",
        "page_start": 425,
        "page_end": 476,
        "sections": [
            {"section_id": "8.1", "title": "Graphing f(x)=ax^2", "page": 425},
            {"section_id": "8.2", "title": "Graphing f(x)=ax^2+c", "page": 431},
            {"section_id": "8.3", "title": "Graphing f(x)=ax^2+bx+c", "page": 437},
            {"section_id": "8.4", "title": "Graphing f(x)=a(x-h)^2+k", "page": 445},
            {"section_id": "8.5", "title": "Using Intercept Form", "page": 453},
            {"section_id": "8.6", "title": "Comparing Linear, Exponential, and Quadratic Functions", "page": 463},
            {"section_id": "8.R", "title": "Chapter Review", "page": 473},
            {"section_id": "8.T", "title": "Practice Test", "page": 476},
        ],
    },
    {
        "chapter_num": 9,
        "title": "Solving Quadratic Equations",
        "page_start": 483,
        "page_end": 540,
        "sections": [
            {"section_id": "9.1", "title": "Properties of Radicals", "page": 483},
            {"section_id": "9.2", "title": "Solving Quadratic Equations by Graphing", "page": 493},
            {"section_id": "9.3", "title": "Solving Quadratic Equations Using Square Roots", "page": 503},
            {"section_id": "9.4", "title": "Solving Quadratic Equations by Completing the Square", "page": 509},
            {"section_id": "9.5", "title": "Solving Quadratic Equations Using the Quadratic Formula", "page": 519},
            {"section_id": "9.6", "title": "Solving Nonlinear Systems of Equations", "page": 529},
            {"section_id": "9.R", "title": "Chapter Review", "page": 537},
            {"section_id": "9.T", "title": "Practice Test", "page": 540},
        ],
    },
    {
        "chapter_num": 10,
        "title": "Radical Functions and Equations",
        "page_start": 547,
        "page_end": 580,
        "sections": [
            {"section_id": "10.1", "title": "Graphing Square Root Functions", "page": 547},
            {"section_id": "10.2", "title": "Graphing Cube Root Functions", "page": 555},
            {"section_id": "10.3", "title": "Solving Radical Equations", "page": 561},
            {"section_id": "10.4", "title": "Inverse of a Function", "page": 569},
            {"section_id": "10.R", "title": "Chapter Review", "page": 577},
            {"section_id": "10.T", "title": "Practice Test", "page": 580},
        ],
    },
    {
        "chapter_num": 11,
        "title": "Data Analysis and Displays",
        "page_start": 587,
        "page_end": 628,
        "sections": [
            {"section_id": "11.1", "title": "Measures of Center and Variation", "page": 587},
            {"section_id": "11.2", "title": "Box-and-Whisker Plots", "page": 595},
            {"section_id": "11.3", "title": "Shapes of Distributions", "page": 603},
            {"section_id": "11.4", "title": "Two-Way Tables", "page": 611},
            {"section_id": "11.5", "title": "Choosing a Data Display", "page": 619},
            {"section_id": "11.R", "title": "Chapter Review", "page": 625},
            {"section_id": "11.T", "title": "Practice Test", "page": 628},
        ],
    },
]


def get_firestore_client():
    try:
        token = subprocess.check_output(["gcloud", "auth", "print-access-token"], text=True).strip()
        creds = Credentials(token)
        return firestore.Client(project=PROJECT_ID, credentials=creds)
    except Exception:
        return firestore.Client(project=PROJECT_ID)


def seed_database():
    print(f"Connecting to Firestore with project ID: '{PROJECT_ID}'...")
    db = get_firestore_client()

    print("Seeding 'curriculum_chapters' collection (Chapters 1-11)...")
    curr_ref = db.collection("curriculum_chapters")
    for ch in CHAPTERS_DATA:
        doc_id = f"chapter-{ch['chapter_num']}"
        curr_ref.document(doc_id).set(ch)
        print(f"  ✓ Seeded Chapter {ch['chapter_num']}: {ch['title']} (p. {ch['page_start']}-{ch['page_end']})")

    print("\nDatabase seeding completed successfully!")


if __name__ == "__main__":
    seed_database()
