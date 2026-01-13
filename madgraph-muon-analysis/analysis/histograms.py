import matplotlib.pyplot as plt
import math
import gzip

# Function to read LHE file 
def read_lhe(filename):
    events = []
    if filename.endswith(".gz"):
        f = gzip.open(filename, 'rt')
    else:
        f = open(filename, 'r')
    
    inside_event = False
    event_data = []
    for line in f:
        if "<event>" in line:
            inside_event = True
            event_data = []
        elif "</event>" in line:
            inside_event = False
            events.append(event_data)
        elif inside_event:
            event_data.append(line.strip())
    f.close()
    return events

# Function to extract muon kinematics
def extract_muon_kinematics(events):
    energies = []
    thetas = []
    pt_list = []
    rapidities = []
    
    for event in events:
        for particle in event[1:]:
            cols = particle.split()
            pid = int(cols[0])
            if abs(pid) == 13:  # muon or anti-muon
                px = float(cols[6])
                py = float(cols[7])
                pz = float(cols[8])
                energy = float(cols[9])
                
                # Kinematics
                p = math.sqrt(px**2 + py**2 + pz**2)
                theta = math.acos(pz / p)        # polar angle
                pt = math.sqrt(px**2 + py**2)    # transverse momentum
                rapidity = 0.5 * math.log((energy + pz)/(energy - pz))  # rapidity
                
                energies.append(energy)
                thetas.append(theta)
                pt_list.append(pt)
                rapidities.append(rapidity)
    
    return energies, thetas, pt_list, rapidities



# Read events
events = read_lhe("data/unweighted_events.lhe.gz")  

# Extract muon kinematics
energies, thetas, pt_list, rapidities = extract_muon_kinematics(events)
thetas_deg = [math.degrees(t) for t in thetas]  # convert to degrees

# PLOT ENERGY
plt.hist(energies, bins=50, color='skyblue', edgecolor='black')
plt.xlabel("Muon Energy [GeV]")
plt.ylabel("Number of Events")
plt.title("Muon Energy Distribution")
plt.savefig("plots/muon_energy_distribution.png")
plt.close()

# PLOT POLAR ANGLE
plt.hist(thetas_deg, bins=50, color='salmon', edgecolor='black')
plt.xlabel("Muon Polar Angle [deg]")
plt.ylabel("Number of Events")
plt.title("Muon Polar Angle Distribution")
plt.savefig("plots/muon_theta_distribution.png")
plt.close()

# PLOT TRANSVERSE MOMENTUM
plt.hist(pt_list, bins=50, color='lightgreen', edgecolor='black')
plt.xlabel("Muon Transverse Momentum pT [GeV]")
plt.ylabel("Number of Events")
plt.title("Muon Transverse Momentum Distribution")
plt.savefig("plots/muon_pt_distribution.png")
plt.close()

#  PLOT RAPIDITY 
plt.hist(rapidities, bins=50, color='violet', edgecolor='black')
plt.xlabel("Muon Rapidity y")
plt.ylabel("Number of Events")
plt.title("Muon Rapidity Distribution")
plt.savefig("plots/muon_rapidity_distribution.png")
plt.show()
