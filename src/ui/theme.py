"""Shared native desktop styling."""

from tkinter import ttk

BACKGROUND = '#f4f6fa'
INK = '#172b4d'
MUTED = '#526176'
BLUE = '#2457d6'


def apply_theme(root):
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure('.', font=('Segoe UI', 10), background=BACKGROUND, foreground=INK)
    style.configure('TFrame', background=BACKGROUND)
    style.configure('TLabel', background=BACKGROUND, foreground=INK)
    style.configure('TButton', padding=(12, 7), background='white', bordercolor='#ccd5e2', cursor='hand2')
    style.map('TButton', background=[('active', '#e9eef9')], bordercolor=[('focus', BLUE)])
    style.configure('Primary.TButton', background=BLUE, foreground='white', font=('Segoe UI', 10, 'bold'))
    style.map(
        'Primary.TButton',
        background=[('disabled', '#c5cee0'), ('active', '#1945b6')],
        foreground=[('disabled', '#526176'), ('!disabled', 'white')],
    )
    style.configure(
        'Nav.TButton', background='#172b4d', foreground='white', borderwidth=0, padding=(14, 12), anchor='w'
    )
    style.map(
        'Nav.TButton', background=[('active', '#294369'), ('focus', '#294369')], foreground=[('!disabled', 'white')]
    )
    style.configure('Card.TFrame', background='white')
    style.configure('Card.TLabel', background='white')
    style.configure('Title.TLabel', font=('Segoe UI', 23, 'bold'))
    style.configure('Section.TLabel', font=('Segoe UI', 11, 'bold'))
    style.configure('Muted.TLabel', foreground=MUTED)
    style.configure('TMenubutton', padding=(10, 7), background='white', bordercolor='#ccd5e2')
    style.map('TMenubutton', background=[('active', '#e9eef9')], bordercolor=[('focus', BLUE)])
    style.configure('TEntry', fieldbackground='white', padding=6, bordercolor='#ccd5e2')
    style.map('TEntry', bordercolor=[('focus', BLUE)])
    style.configure('TCombobox', padding=6, fieldbackground='white')
    style.configure('Treeview', background='white', fieldbackground='white', rowheight=30)
    style.configure('TLabelframe', background=BACKGROUND, bordercolor='#dce2eb')
    style.configure('TLabelframe.Label', background=BACKGROUND, foreground=MUTED)
    style.configure('Horizontal.TProgressbar', background=BLUE)
