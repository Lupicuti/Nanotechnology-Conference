import os

files_to_check = [
    'index.html',
    'workshops.html',
    'server.py',
    'registration.html',
    'admin.html',
    'generate_workbook.py',
    'conference_poster.html'
]

for filename in files_to_check:
    if not os.path.exists(filename): continue
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix Marta De Luca's abstract by adding the quote
    content = content.replace(
        'by using optical nanospectroscopy, probe the optical resonances in a nanowire cavity, and play with different refractive indexes, cavity lengths and gain media to create your nanolaser.',
        'by using optical nanospectroscopy, probe the optical resonances in a nanowire cavity, and play with different refractive indexes, cavity lengths and gain media to create your nanolaser".'
    )
    
    # Also in case I wrote it without period
    content = content.replace(
        '<p>by using optical nanospectroscopy, probe the optical resonances in a nanowire cavity, and play with different refractive indexes, cavity lengths and gain media to create your nanolaser</p>',
        '<p>by using optical nanospectroscopy, probe the optical resonances in a nanowire cavity, and play with different refractive indexes, cavity lengths and gain media to create your nanolaser".</p>'
    )
    
    # Fix Laboratory name
    content = content.replace('Micro-Raman Lab (Sapienza)', 'Nanospectroscopy (Sapienza)')
    content = content.replace('Micro-Raman Lab', 'Nanospectroscopy')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updates applied.")
