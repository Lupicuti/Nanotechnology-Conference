import os
import re

files_to_check = [
    'index.html',
    'workshops.html',
    'server.py',
    'registration.html',
    'admin.html',
    'generate_workbook.py',
    'conference_poster.html'
]

replacements = {
    'Nanomedicine Experience': 'Amphiphile-Based Nanomedicines: Principles, Rational Design, and Characterization',
    'Semiconductor Nanowires': 'Try turning a semiconductor nanowire into a nanolaser !',
    'Light and Photonics': 'Coupling light-emitting 2D materials with on-chip photonic circuits'
}

descriptions_workshops = {
    'Design, synthesis, and characterization of advanced lipid/polymer\n                                nanocarriers and targeted drug delivery vesicles.': 'The practical sessions will open with an introductory overview of nanocarrier fundamentals and the relevant theoretical background. In the laboratory, students will observe a rational design approach, formulating, purifying, and characterizing several types of nanocarriers obtained through different preparation methods, all starting from the same surfactant. This will illustrate how a single set of starting materials can be strategically tailored to yield distinct nanostructures, depending on the intended therapeutic application.',
    
    'Investigate the optical and vibrational properties of 1D semiconductor\n                                nanowires using micro-Raman and photoluminescence spectroscopy.': 'by using optical nanospectroscopy, probe the optical resonances in a nanowire cavity, and play with different refractive indexes, cavity lengths and gain media to create your nanolaser.',
    
    'Characterizing electronic and optical behavior of custom nanostructures\n                                for next-generation optoelectronic integrated circuits.': 'During this interactive laboratory demonstration, participants will explore how laser power, temperature, and excitation-spot position affect the intensity of the light emitted by a two-dimensional crystal and coupled into a lithographically defined photonic waveguide.'
}

descriptions_index = {
    'Design, synthesis, and characterization of advanced lipid/polymer nanocarriers and targeted drug\n                        delivery vesicles for innovative therapeutics.': 'The practical sessions will open with an introductory overview of nanocarrier fundamentals and the relevant theoretical background. In the laboratory, students will observe a rational design approach, formulating, purifying, and characterizing several types of nanocarriers obtained through different preparation methods, all starting from the same surfactant. This will illustrate how a single set of starting materials can be strategically tailored to yield distinct nanostructures, depending on the intended therapeutic application.',
    
    'Investigate the optical and vibrational properties of 1D semiconductor nanowires using micro-Raman\n                        and photoluminescence spectroscopy for nanophotonic devices.': 'by using optical nanospectroscopy, probe the optical resonances in a nanowire cavity, and play with different refractive indexes, cavity lengths and gain media to create your nanolaser.',
    
    'Characterizing electronic and optical behavior of custom nanostructures for next-generation\n                        optoelectronic integrated circuits and light emission.': 'During this interactive laboratory demonstration, participants will explore how laser power, temperature, and excitation-spot position affect the intensity of the light emitted by a two-dimensional crystal and coupled into a lithographically defined photonic waveguide.'
}

for filename in files_to_check:
    if not os.path.exists(filename): continue
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Apply specific description replacements first
    for old, new in descriptions_workshops.items():
        content = content.replace(old, new)
        
    for old, new in descriptions_index.items():
        content = content.replace(old, new)

    # Apply title replacements
    for old, new in replacements.items():
        content = content.replace(old, new)

    # Manual specific overrides for seats that need regex or careful replacement
    # Workshops.html seats for Nanowires
    content = re.sub(r'Seats: <b>6 / 15 remaining</b>', r'Seats: <b>10 / 10 remaining</b>', content)
    # Index.html JS max seats for Nanowires
    content = re.sub(r"\'nanowires\': \{ name: \'.*?\', max: 15 \}", r"'nanowires': { name: 'Try turning a semiconductor nanowire into a nanolaser !', max: 10 }", content)

    # Workshops.html seats for Photonics
    content = re.sub(r'Seats: <b>5 / 15 remaining</b>', r'Seats: <b>6 / 6 remaining</b>', content)
    # Index.html JS max seats for Photonics
    content = re.sub(r"\'photonics\': \{ name: \'.*?\', max: 15 \}", r"'photonics': { name: 'Coupling light-emitting 2D materials with on-chip photonic circuits', max: 6 }", content)

    # The user says Fabiano is 15. The JS might say max: 15. 
    content = re.sub(r"\'nanomedicine\': \{ name: \'.*?\', max: \d+ \}", r"'nanomedicine': { name: 'Amphiphile-Based Nanomedicines: Principles, Rational Design, and Characterization', max: 15 }", content)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Replacements done.")
