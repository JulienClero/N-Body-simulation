import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tqdm import tqdm
import conversion as conv
import get_initial_conditions as gic
import tkinter as tk
import tkinter.ttk as ttk

G = 6.674184e-11
c = 299792458
R = 6.371e6


window = tk.Tk()
window.title("Simulation à N-corps")
window.geometry("1000x320")

#https://ssd.jpl.nasa.gov/horizons/app.html#/  | Je me suis servi de ce site pour générer les conditions initales des corps que l'on simule. 
#Les données initiales étaient donné en Km , km/s je copiais collais donc en ajoutant 3 a l'exposant de la puissance de 10. Puisque le simulateur est basé sur les unités SI de base, a savoir : m , s , kg...
#Je m'attendais a ce que trouver des données de qualité soit plus dur mais non seulement elles étaitent accessible mais elles collaient aussi parfaitement avec le fonctionnement du simulateur. (Coordonnées cartésiennes avec pour centre le barycentre du système solaire)
#Coordinate Center: Solar System Barycenter (SSB) [500@0]

#https://ssd.jpl.nasa.gov/planets/eph_export.html
#https://ssd.jpl.nasa.gov/ephem.html

theta = 19.955 #Pour Apollo 13, trouvé par tatonnement.
phi = 2.565 #Pour Apollo 13, trouvé par tatonnement.

selection = [
[   {'name': 'Système Solaire | Satellites de Jupiter (pas = 2H, 6mois)', 'step' : 3600, 'span' : 86000*365*2,'speed' : 1},
    {'name': 'Soleil', 'mass': 1.9891e30, 'initial_position': [0, 0,0], 'initial_velocity': [0, 0,0], 'radius': 6.957e8, 'color': 'yellow', 'alpha': 1000},
    {'name': 'Mercure', 'mass': 3.285e23, 'initial_position': [3.111326828211597e10, -5.728341483959676e10,-7.535075582470600e9], 'initial_velocity': [3.306665084735877e4, 2.566616097807606e4,-9.355134375548673e2], 'radius': 2440.5e6, 'color': '#a8a8a8', 'alpha': 200},
    {'name': 'Venus', 'mass': 4.8673e24, 'initial_position': [8.160003631559227e10, 7.097851221504661e10,-3.733598399489257e9], 'initial_velocity': [-2.308967357673062e4, 2.627389648726430e4,1.693128996733767e3], 'radius': 6051.8e6, 'color': '#e5d7a0', 'alpha': 200},
    {'name': 'Terre', 'mass': 5.972e24, 'initial_position': [-8.818337040722354e10, -1.228484260446720e11,7.029978363126516e6], 'initial_velocity': [2.372298820740589e4, -1.747547835352001e4,1.413007463911597e0], 'radius': R, 'color': '#0080ff', 'alpha': 200},
    {'name': 'Mars', 'mass': 6.39e23, 'initial_position': [1.945752019226745e11, -6.952273536172792e10,-6.229648433382463e9], 'initial_velocity': [9.075485314434678e3, 2.488578017706407e4,2.989334059210886e2], 'radius': 3396.2e6, 'color': '#ff5733', 'alpha': 200},
	{'name': 'Jupiter', 'mass': 1898.13e24, 'initial_position': [4.015145548397205e11, 6.336198517651941e11,-1.161519024058139e10], 'initial_velocity': [-1.119862866249050e4, 7.615886058929404e3,2.188841306452334e2], 'radius': 71.492e6, 'color': '#ffd700', 'alpha': 200},
    {'name': 'Saturn', 'mass': 5.6834e26, 'initial_position': [1.378490561825825e12, -4.503789156433709e11, -4.703076790132886e10], 'initial_velocity': [2.456221253758718e3, 9.172206876131931e3, -2.578716239220635e2], 'radius': 58232e3, 'color': '#cdcdcd', 'alpha': 200},
    #{'name': 'Sagittarius A*', 'mass': 4.297e6*1.9891e30, 'initial_position': [0, 0,-2.52318e+20], 'initial_velocity': [0, 0,0], 'radius': R, 'color': 'k', 'alpha': 20000},
	
    # Satellites de Jupiter
	
    {'name': 'Io', 'mass': 8.9319e22, 'initial_position': [4.019262149420174e11,6.337078524915825e11,-1.160611834835866e10], 'initial_velocity': [-1.477340247693827e4, 2.460139080971030e4,7.648120766668125e2], 'radius': R, 'color': 'cyan', 'alpha': 1000},
	{'name': 'Callisto', 'mass': 1.0759e23, 'initial_position': [3.996630215216969e11, 6.332110609552279e11,-1.165276597358423e10], 'initial_velocity': [-9.434677199985762e3, -3.316101380114013e2,-6.337431457758835e0], 'radius': R, 'color': 'g', 'alpha': 1000},
	{'name': 'Ganymede', 'mass': 1.4819e23, 'initial_position': [4.008496881300144e11, 6.327816143835790e11,-1.165655901799959e10], 'initial_velocity': [-2.658559544439814e3,8.815356722574557e2,8.280609362941532e1], 'radius': R, 'color': 'brown', 'alpha': 1000},
	{'name': 'Europe', 'mass': 4.7998e22, 'initial_position': [4.021409520325906e11, 6.333652245320718e11,-1.160977776905644e10], 'initial_velocity': [-6.138129652460865e3, 2.026906098142650e4,7.555812123002834e2], 'radius': R, 'color': 'white', 'alpha': 1000},
],
[   {'name': 'Système Solaire 250 ans terrestre', 'step' : 86000*5, 'span' : 86000*365*250,'speed' : 4},
    {'name': 'Soleil', 'mass': 1.9891e30, 'initial_position': [0, 0,0], 'initial_velocity': [0, 0,0], 'radius': 6.957e8, 'color': 'yellow', 'alpha': 1000},
    {'name': 'Mercure', 'mass': 3.285e23, 'initial_position': [3.111326828211597e10, -5.728341483959676e10,-7.535075582470600e9], 'initial_velocity': [3.306665084735877e4, 2.566616097807606e4,-9.355134375548673e2], 'radius': 2440.5e6, 'color': '#a8a8a8', 'alpha': 2},
    {'name': 'Venus', 'mass': 4.8673e24, 'initial_position': [8.160003631559227e10, 7.097851221504661e10,-3.733598399489257e9], 'initial_velocity': [-2.308967357673062e4, 2.627389648726430e4,1.693128996733767e3], 'radius': 6051.8e6, 'color': '#e5d7a0', 'alpha': 2},
    {'name': 'Terre', 'mass': 5.972e24, 'initial_position': [-8.818337040722354e10, -1.228484260446720e11,7.029978363126516e6], 'initial_velocity': [2.372298820740589e4, -1.747547835352001e4,1.413007463911597e0], 'radius': R, 'color': '#0080ff', 'alpha': 2},
    {'name': 'Mars', 'mass': 6.39e23, 'initial_position': [1.945752019226745e11, -6.952273536172792e10,-6.229648433382463e9], 'initial_velocity': [9.075485314434678e3, 2.488578017706407e4,2.989334059210886e2], 'radius': 3396.2e6, 'color': '#ff5733', 'alpha': 2},
	{'name': 'Jupiter', 'mass': 1.89813e27, 'initial_position': [4.015145548397205e11, 6.336198517651941e11,-1.161519024058139e10], 'initial_velocity': [-1.119862866249050e4, 7.615886058929404e3,2.188841306452334e2], 'radius': 71.492e6, 'color': '#ffd700', 'alpha': 100},
    {'name': 'Saturn', 'mass': 5.6834e26, 'initial_position': [1.378490561825825e12, -4.503789156433709e11, -4.703076790132886e10], 'initial_velocity': [2.456221253758718e3, 9.172206876131931e3, -2.578716239220635e2], 'radius': 58232e3, 'color': '#e6e8fa', 'alpha': 500},
    {'name': 'Uranus','mass': 8.681e25,'initial_position': gic.get_stats("Uranus.txt")['initial_position'],'initial_velocity': gic.get_stats("Uranus.txt")['initial_velocity'],'radius': 25362.0e3,'color': '#b0e0e6','alpha': 2500},
    {'name': 'Neptune','mass': 1.024e26,'initial_position': gic.get_stats("Neptune.txt")['initial_position'],'initial_velocity': gic.get_stats("Neptune.txt")['initial_velocity'],'radius': 24622.0e3,'color': '#00008b','alpha': 5000},
    {'name': 'Pluton', 'mass': 1.307e22, 'initial_position': gic.get_stats("Pluton.txt")['initial_position'], 'initial_velocity': gic.get_stats("Pluton.txt")['initial_velocity'], 'radius': 1188.3e3, 'color': '#a97142', 'alpha': 50000},
    
],
[   {'name': 'Trou Noir Voie Lactée', 'step' : 1, 'span' : 86000,'speed' : 1},
    {'name': 'Sagittarius A*', 'mass': 4.297e6*1.9891e30, 'initial_position': [0, 0,0], 'initial_velocity': [0, 0,0], 'radius': R, 'color': 'k', 'alpha': 20000},
    {'name': 'Photon', 'mass': 0, 'initial_position': [6.5e9, 0,0], 'initial_velocity': [0, 299792458,0], 'radius': 6.957e8, 'color': 'white', 'alpha': 100},
],
[   {'name': 'Voyager 2 | Début : 30-07-1977 (dt = 6H)', 'step' : 86000//6, 'span' : 86000*365*4,'speed' : 5},
    {'name': 'Soleil', 'mass': 1.9891e30, 'initial_position': [0, 0,0], 'initial_velocity': [0, 0,0], 'radius': 6.957e8, 'color': 'yellow', 'alpha': 1000},
    {'name': 'Mercure', 'mass': 3.285e23, 'initial_position': [4.585851671127070E+10, -4.036878632449235E+10,-7.508263431018079E+09], 'initial_velocity': [2.255643032394270E+04, 3.886197072782283E+04,1.101805472241903E+03], 'radius': 2440.5e6, 'color': '#a8a8a8', 'alpha': 25},
    {'name': 'Venus', 'mass': 4.8673e24, 'initial_position': [3.915210665888662E+10, 1.005073031327420E+11,-8.931278514552042E+08], 'initial_velocity': [-3.274923590551895E+04, 1.254781223098944E+04,2.061661065146139E+03], 'radius': 6051.8e6, 'color': '#e5d7a0', 'alpha': 25},
    {'name': 'Terre', 'mass': 5.972e24, 'initial_position': [1.388514184769984E+11, -5.942799354793376E+10,-2.414887408047915E+06], 'initial_velocity': [1.123399246997738E+04, 2.726296277559703E+04, 2.397043383668418E-0], 'radius': R, 'color': '#0080ff', 'alpha': 25},
    {'name': 'Mars', 'mass': 6.39e23, 'initial_position': [1.425621369613381E+11, 1.678158768990914E+11,2.912100175291300E+06], 'initial_velocity': [-1.753890503915145E+04, 1.774649460691353E+04,8.035685412287794E+02], 'radius': 3396.2e6, 'color': '#ff5733', 'alpha': 25},
	{'name': 'Jupiter', 'mass': 1898.13e24, 'initial_position': [1.126304934545872E+11, 7.538657472688994E+11,-5.623229883170485E+09], 'initial_velocity': [-1.308812145910008E+04, 2.540656473180508E+03,2.827140914305026E+2], 'radius': 71.492e6, 'color': '#ffd700', 'alpha': 1000},
    {'name': 'Saturn', 'mass': 5.6834e26, 'initial_position': [-1.072193875213905E+12, 8.584088434289923E+11,  2.760005560729045E+10], 'initial_velocity': [-6.571489714479159E+03, -7.565911911870572E+03, 3.930609470853317E+2], 'radius': 58232e3, 'color': '#cdcdcd', 'alpha': 1000},
    
    {'name': 'Voyager 2', 'mass': 721.9, 'initial_position': [1.407517971771144E+11, -5.190876855563348E+10,2.627190842614127E+09], 'initial_velocity': [1.350199806495103E+04, 3.649368033922408E+04, 3.215596528358999E+03], 'radius': 4, 'color': 'magenta', 'alpha': 5000},
],
[
    {'name': 'Terre-Lune', 'step' : 3600, 'span' : 86000*30,'speed' : 1},
    {'name': 'Terre', 'mass': 5.972e24, 'initial_position': [0, 0,0], 'initial_velocity': [0, 0,0], 'radius': R, 'color': '#0080ff', 'alpha': 20000},
    {'name': 'Lune', 'mass': 0.07346e24, 'initial_position': [0.3633e9, 0,0], 'initial_velocity': [0, 1.082e3,0], 'radius': 1.7e6, 'color': 'grey', 'alpha': 20000},
],
[
    {'name': 'Apollo 13', 'step' : 50, 'span' : 86000*11,'speed' : 20},
    {'name': 'Terre', 'mass': 5.972e24, 'initial_position': [0, 0,0], 'initial_velocity': [0, 0,0], 'radius': R, 'color': '#0080ff', 'alpha': 50},
    {'name': 'Lune', 'mass': 0.07346e24, 'initial_position': [-3.598026586164881e8, 1.807371975963677e8,5.155224188183769e6], 'initial_velocity': [-4.160024446675525e2,-8.765413945648834e2,-8.716563534876892e1], 'radius': 1.7e6, 'color': 'grey', 'alpha': 5000},
    {'name': 'Apollo 13', 'mass':  2000, 'initial_position': [(R+2.191e6)*np.cos(conv.deg_to_rad(theta)), (R+2.191e6)*np.sin(conv.deg_to_rad(theta)),(R+2.191e6)*np.sin(conv.deg_to_rad(phi))], 'initial_velocity': [(9.574e3)*np.cos(conv.deg_to_rad(90+theta)), (9.574e3)*np.sin(conv.deg_to_rad(90+theta)), 0], 'radius': 50, 'color': 'k', 'alpha': 5000, 'drag':0.15},
],
[
    {'name': 'Orbite carrée', 'step' : 3600*4, 'span' : 86000*365*4,'speed' : 10},
    {'name': 'Étoile', 'mass': 1.003673e30, 'initial_position': [0, 0,0], 'initial_velocity': [0, 0,0], 'radius': 6.957e8, 'color': 'r', 'alpha': 500},
    {'name': 'Planète', 'mass': 1.434416e28, 'initial_position': [300e9, 0,0], 'initial_velocity': [0,np.sqrt((G*1.003673e30)/300e9),0], 'radius': R, 'color': 'yellow', 'alpha': 5000},
    {'name': 'Satellite', 'mass':  2000, 'initial_position': [300e9 - 35e9, 0,0], 'initial_velocity': [0,np.sqrt((G*1.003673e30)/(300e9-35e9))-np.sqrt((G*1.434416e28)/(35e9))+225,0], 'radius': 50, 'color': 'k', 'alpha': 5000},
],]

############################################################################################# Simulation (Calcul des positions et vitesses)

def rho(h):    
    return 1.39*np.exp(-(h)/7900)

def f(X):
    result = np.zeros(mh)
    
    for i in range(len(corps_stat)):
        for j in range(len(corps_stat)):
            if corps_stat[j]['mass'] < 1e10: # On néglige l'influence des corps peu massif
                break
            if j != i:          
                pos1 = X[mh//2 + 3*i : mh//2 + 3 + 3*i]
                pos2 = X[mh//2 + 3*j : mh//2 + 3 + 3*j]

                d = np.sqrt(np.sum((pos2 - pos1) ** 2))
                
                k = G/(d**3)
                
                result[3*i:3 + 3*i] += k * corps_stat[j]['mass'] * (pos2 - pos1)
                result[mh//2 + 3*i: mh//2 + 3 + 3*i] = X[3*i:3 + 3*i]

                if d <= corps_stat[i]['radius']+corps_stat[j]['radius'] :
                     
                     return True

                if d <= R+100e6 and corps_stat[i]['name'] == "Terre":                  
                     result[3*j:3 + 3*j] += (G * corps_stat[j]['mass'] * (pos2 - pos1) / (d**3)) - corps_stat[j]['drag']*rho(d-R)*X[3*j:3 + 3*j]
                     result[mh//2 + 3*i: mh//2 + 3 + 3*i] = X[3*i:3 + 3*i]
                     
            
    return result

def run_simulation(corps_stat,Y,h,RKX):  #bodies_data est un dictionnaire contenant les informations sur les corps sujets a la résolution. h le pas.
    
    RKX
    n = 0
    for corps in corps_stat: #Conditions initiales

        Y[0+3*n:3+3*n, 0] = corps['initial_velocity']
        Y[mh//2 + 3*n : mh//2 + 3 + 3*n, 0] = corps['initial_position']
        
        n += 1
    n = 0
    if RKX == "RK4":
        
        for i in tqdm(range(len(t)-1)): #Itérations RK4
            if type(f(Y[:,i])) == bool:
                    break
    
            k1 = f(Y[:,i])
            k2 = f(Y[:,i] + (h/2) * k1)
            k3 = f(Y[:,i] + (h/2) * k2)
            k4 = f(Y[:,i] + h * k3)
    
            Y[:,i+1] = Y[:,i] + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
    
    elif RKX == "RK2":
        
        for i in tqdm(range(len(t)-1)): #Itérations RK2
            if type(f(Y[:,i])) == bool:
                    break
                
            k1 = f(Y[:,i])
            k2 = f(Y[:,i] + h * k1)  
            
            Y[:,i+1] = Y[:,i] + (h/2) * (k1 + k2)
    
    return Y[:,0:i]

############################################################################################# UI

def pos_in_grid(n):
    
    row = n // 3 + 1
    column = n % 3 + 1
    return row-1, column-1

def select(option):
    def init():
        global choice
        global RKX
        if option in presets:
            choice = option
            remove_buttons()  
            create_new_buttons()
        elif option == "RK4" :
            RKX = "RK4"
            window.destroy()
        elif option == "RK2":
            RKX = "RK2"
            window.destroy()
    return init

def remove_buttons():
    for button in buttons:
        button.grid_forget()

def create_new_buttons():   
    new_buttons = [
        ttk.Button(window, text="RK2", command= select("RK2")),
        ttk.Button(window, text="RK4", command= select("RK4")),
        # Ajoutez autant de boutons que nécessaire pour vos nouveaux choix
    ]
    
    new_buttons[0].grid(row=1, column=0, sticky="nwse")
    new_buttons[1].grid(row=1, column=2, sticky="nwse")

############################### Tkinter

presets = {}
for sous_liste in selection:

    presets[sous_liste[0]['name']] = sous_liste
for i in range(0, 3):
    window.columnconfigure(i, weight=1,uniform="same")
for i in range(0, 3):
    window.rowconfigure(i, weight=1,uniform="same")

buttons = []
for i in range(len(selection)):
    buttons.append(ttk.Button(window, text=f"{selection[i][0]['name']}", command= select(selection[i][0]['name'])))

for i in range(len(buttons)):
    buttons[i].grid(row=pos_in_grid(i)[0], column=pos_in_grid(i)[1], sticky="nwse")
 
window.mainloop()  

############################################################################################# Initialisation

sim_data = presets[choice] #Données des corps et de la simulation
corps_stat = presets[choice][1:]  #Données des corps unqiuement 
mh  = len(corps_stat) * 6
h = sim_data[0]['step']
temps = sim_data[0]['span']
vitesse_sim = sim_data[0]['speed']
txt_offset = 20*R   
t = np.arange(0,temps,h)
Y = np.zeros([mh,len(t)])
A = []
for i in corps_stat:        
    A.append(np.sqrt(i['initial_position'][0]**2+i['initial_position'][1]**2+i['initial_position'][2]**2))
    size = max(A)
Y = run_simulation(corps_stat, Y,h,RKX)

############################### Analyse des calculs

vitesses = np.zeros([len(corps_stat),len(Y[0,:])])
vit_max = []
for corps in range(len(corps_stat)):
    for i in range(len(Y[0,:])):
        vitesses[corps,i] = np.sqrt(Y[3*(corps),i]**2 + Y[3*(corps)+1,i]**2 + Y[3*(corps)+2,i]**2)       
    vit_max.append(max(vitesses[corps]))


distances = np.zeros([len(corps_stat),len(corps_stat),len(Y[0,:])])
dist_min = np.zeros([len(corps_stat),len(corps_stat)])
used = [] #used sert répertorier les corps qui sont déja passés dans la boucle for pour permettre la détection des combinaisons déja utilisées.
for corps1 in range(len(corps_stat)):
    if corps1 not in used:
        used.append(corps1)
        for corps2 in range(len(corps_stat)):
            if corps2 not in used:
                if corps1 != corps2:
                    for i in range(len(Y[0,:])):
                
                        pos1 = Y[mh//2 + 3*(corps1):mh//2 + 3*(corps1)+3,i]
                        pos2 = Y[mh//2 + 3*(corps2):mh//2 + 3*(corps2)+3,i]
            
                        d = np.sqrt(np.sum((pos2 - pos1) ** 2))
                
                        distances[corps1,corps2,i] = d
                        if d <= corps_stat[corps1]['radius']+corps_stat[corps2]['radius'] :
                            print(f"Collision between {corps_stat[corps1]['name']} and {corps_stat[corps2]['name']}")
                        
                    dist_min[corps1,corps2] = min(distances[corps1,corps2])


used = []                
for i in range(len(corps_stat)):
    if i not in used:
        used.append(i)
        for j in range(len(corps_stat)):  
            if j not in used:
                if dist_min[i,j] <= 300e6*10:   # Le message s'affiche que si la distance entre les 2 corps est inférieure à la distance Terre-Lune.
                    print(f"Distance minimale entre les centres de {corps_stat[i]['name']}  et de {corps_stat[j]['name']}: {dist_min[i,j]/1e3:.2f} km")
                    print(f"Distance minimale entre la surface de {corps_stat[i]['name']}  et celle de {corps_stat[j]['name']}: {(dist_min[i,j]- corps_stat[i]['radius'] - corps_stat[j]['radius'])/1e3:.2f} km")

for i in range(len(corps_stat)):        
    
    if (vit_max[i]/299792458)*100 >= 1:       
        print(f"Vitesse maximale de/du/de la {corps_stat[i]['name']} : {vit_max[i]:.2f} m/s  soit  {(vit_max[i]/c)*100:.10f}% de c")
        if (vit_max[i]/299792458)*100 > 100:
            print("Plus rapide que la lumière")          
    else :
        print(f"Vitesse maximale de/du/de la {corps_stat[i]['name']} : {vit_max[i]:.2f} m/s")
    if (vit_max[i]/299792458)*100 >= 5 and vit_max[i] < c:      
        dtr = 3600/np.sqrt(1-(vit_max[i]**2)/(c**2))        
        print(f"A cette vitesse : 1 Heure = {dtr/3600} Heure(s)")
        
           
############################################################################################# Animation

def update(frame):
    for i in range(len(corps_stat)):
        if frame <= corps_stat[i]['alpha']:
            bodies[i].set_data_3d(Y[mh//2 + 3*i : mh//2 + 3*(i+1), 0:frame*vitesse_sim ])
        else:
            bodies[i].set_data_3d(Y[mh//2 + 3*i : mh//2 + 3*(i+1), (frame-corps_stat[i]['alpha'])*vitesse_sim:frame*vitesse_sim  ])
        
        txt[i].set_position((Y[mh//2 + 3*i, frame*vitesse_sim] + txt_offset,
                             Y[mh//2 + 3*i + 1, frame*vitesse_sim ] + txt_offset,
                             Y[mh//2 + 3*i + 2, frame*vitesse_sim ]))

    return bodies + txt 

fig = plt.figure(figsize=(15, 15))
ax = fig.add_subplot(111, projection='3d')

ax.set_box_aspect([1, 1, 1])
ax.axis('equal')   
ax.axis('off')

ax.set_facecolor('#3d3d3d')

ax.set_xlim(-size, size)
ax.set_ylim(-size, size)
ax.set_zlim(-size, size)

bodies = []
txt = []

for i in range(len(corps_stat)):
    
    bodies.append(ax.plot([], [], [], color=corps_stat[i]['color'], linewidth=1)[0])
    txt.append(ax.text(Y[mh//2 + 3*i,0], Y[mh//2 + 3*i + 1,0], Y[mh//2 + 3*i + 2,0], f'({corps_stat[i]["name"]})', color=corps_stat[i]['color'], fontsize=6))        #f'({bodies_data[i]["name"]})'

ani = FuncAnimation(fig, update, frames=len(Y[0,:])//vitesse_sim, interval=0, blit=True)

plt.show()