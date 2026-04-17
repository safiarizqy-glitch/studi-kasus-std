import tkinter as tk
from tkinter import ttk, messagebox

data_mahasiswa = []
kotak_visual = []
delay, step_count = 600, 0

def render_visual(active_left=None, active_right=None, found=None, passed=None):
    for w in kotak_visual: w.destroy()
    kotak_visual.clear()
    for i, (nim, _) in enumerate(data_mahasiswa):
        warna = "#094D0C" 
        if passed and i in passed: warna = "#CAB5AF"
        if i == active_left: warna = "#A3D1F7"
        if i == active_right: warna = "#E2A1EE"
        if i == found: warna = "#FF05FF"
        
        f = tk.Frame(frame_visual, bg=warna, bd=2, relief="solid")
        f.pack(side="left", padx=3, pady=10)
        tk.Label(f, text=str(nim), bg=warna, width=7, font=("Arial", 9, "bold")).pack()
        tk.Label(f, text=str(i), bg=warna, font=("Arial", 8)).pack()
        kotak_visual.append(f)

def tambah_data():
    try:
        nim, nama = int(entry_nim.get()), entry_nama.get()
        if not nama: raise ValueError
        if any(row[0] == nim for row in data_mahasiswa):
            return messagebox.showerror("Duplikat", f"NIM {nim} sudah ada!")
        data_mahasiswa.append([nim, nama])
        data_mahasiswa.sort()
        refresh_ui()
    except: messagebox.showwarning("Inputan", "Data tidak valid!")

def refresh_ui():
    for item in tree.get_children(): tree.delete(item)
    for row in data_mahasiswa: tree.insert("", "end", values=row)
    render_visual()

def animasi_binary(steps, hasil, step=0, passed=None):
    global step_count
    if step == 0: 
        step_count, passed = 0, set()
    
    if step >= len(steps):
        msg = f"Ditemukan: {data_mahasiswa[hasil][1]}" if hasil != -1 else "Tidak Ada"
        return lbl_status.config(text=f"{msg} | Total Steps: {step_count}")

    s = steps[step]
    step_count += 1
    lbl_status.config(text=f"Step {step_count}: Memeriksa Indeks {s['m']} (NIM: {s['v']})")
    render_visual(active_left=s['l'], active_right=s['r'], passed=passed)
    passed.update(range(s['l'], s['r']+1))
    root.after(delay, lambda: animasi_binary(steps, hasil, step+1, passed))

def cari_binary():
    try:
        target = int(entry_cari.get())
        l, r, steps = 0, len(data_mahasiswa)-1, []
        while l <= r:
            m = (l + r) // 2
            steps.append({'l':l, 'm':m, 'r':r, 'v':data_mahasiswa[m][0]})
            if data_mahasiswa[m][0] == target: 
                return animasi_binary(steps, m)
            if data_mahasiswa[m][0] < target: l = m + 1
            else: r = m - 1
        animasi_binary(steps, -1)
    except: messagebox.showerror("Error", "Inputin NIM!")

# ========== GUI SETUP ===========
root = tk.Tk()
root.title("Binary Search Visual")
root.geometry("950x550")

tk.Label(root, text="BINARY SEARCH", font=("Arial", 16, "bold"), bg="#41AAFF", fg="white").pack(fill="x")

def create_entry(parent, label, width):
    tk.Label(parent, text=label).pack(side="left", padx=2)
    e = tk.Entry(parent, width=width)
    e.pack(side="left", padx=5)
    return e

f_in = tk.Frame(root); f_in.pack(pady=10)
entry_nim = create_entry(f_in, "NIM:", 10)
entry_nama = create_entry(f_in, "Nama:", 15)
tk.Button(f_in, text="Tambah", command=tambah_data, bg="#98F59B", fg="white").pack(side="left")

f_sh = tk.Frame(root); f_sh.pack(pady=5)
entry_cari = create_entry(f_sh, "Cari NIM:", 10)
tk.Button(f_sh, text="Cari", command=cari_binary, bg="#FFBB54", fg="white").pack(side="left", padx=2)
tk.Button(f_sh, text="Reset", command=lambda: [lbl_status.config(text="Siap..."), render_visual()], bg="#EEC9C9").pack(side="left")

lbl_status = tk.Label(root, text="Siap pencarian", font=("Arial", 11, "bold"), bg="#A1C9E6", relief="ridge", pady=5)
lbl_status.pack(fill="x", padx=20, pady=5)

frame_visual = tk.Frame(root, height=120, bg="#a16868", relief="ridge", bd=2)
frame_visual.pack(fill="x", padx=20); frame_visual.pack_propagate(False)

tree = ttk.Treeview(root, columns=("NIM", "Nama"), show="headings", height=10)
for c in ("NIM", "Nama"): tree.heading(c, text=c)
tree.pack(fill="both", expand=True, padx=20, pady=10)

refresh_ui()
root.mainloop()