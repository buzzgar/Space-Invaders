### **📜 Cosmic Conquistadors - README**  

# 🌌 Cosmic Conquistadors - Group Project

## 📌 Project Overview  
Cosmic Conquistadors is a **Space Invaders-inspired** game developed for **Computer Science E214 (2025)**.  

**🗓 Deadline:** April 25, 2025, at 11:59 AM (SunLearn Submission)  
**🎮 Demo Date:** April 29, 2025 (Compulsory)  

---

## 🎯 Goals & Minimum Requirements (60%)  
To score the **minimum 60%**, the game must have:  

- [ ] **Title Screen** with instructions (Press `Space` to start).  
- [ ] **Shooter movement** (left & right) within screen boundaries.  
- [ ] **Turret rotation** (cannot aim below horizontal).  
- [ ] **Missiles fire** from the turret at an angle.  
- [ ] **Enemies move in a grid**, shifting left-right and descending.  
- [ ] **Missile collision detection** (destroy enemy on hit).  
- [ ] **Score display** (increases when enemies are destroyed).  
- [ ] **Game Over conditions**:  
  - [ ] Win when all enemies are destroyed.  
  - [ ] Lose if an enemy reaches the ground or touches the shooter.  
  - [ ] "Game Over" screen appears before restart.  
- [ ] **Game restarts** automatically after a short delay.  
- [ ] **Quit option (`q` key)** to exit the game.  

---

## 🏆 Bonus Features (Extra 40%)  
To maximize the **final 100% score**, add these enhancements:  

### 🎨 **Visual & UI Improvements**  
- [ ] Improved **graphics & animations** (custom sprites, effects).  
- [ ] Enhanced **background & UI elements**.  

### 🔊 **Audio Enhancements**  
- [ ] **Sound effects** for shooting & enemy destruction.  
- [ ] **Background music** for better immersion.  

### ⚔️ **Gameplay Upgrades**  
- [ ] **High score leaderboard** displayed after game over.  
- [ ] **Progressive difficulty** (faster enemies, more aggressive AI).  
- [ ] **Multiple lives** & increasing challenge per level.  
- [ ] **Two-player mode** (competitive or co-op).  
- [ ] **Enemies counterattack** (drop bombs).  
- [ ] **Bunkers & shields** for defense.  
- [ ] **Power-ups** (faster shooting, stronger missiles).  

---

## 🔧 Development Plan  

### ✅ **Phase 1: Core Mechanics (Weeks 1-3)**
- [ ] Implement **title screen & UI**.  
- [ ] Create **basic shooter movement**.  
- [ ] Implement **basic enemy behavior** (movement & descent).  

### 🚀 **Phase 2: Game Logic (Weeks 4-5)**  
- [ ] Implement **OOP structure** (Shooter, Enemies, Missiles as objects).  
- [ ] Add **scoring system & win/loss conditions**.  
- [ ] Implement **missile collision detection**.  

### 🎨 **Phase 3: Enhancements & Polish (Final Weeks)**  
- [ ] Improve **graphics & animations**.  
- [ ] Add **sound effects & music**.  
- [ ] Test & **debug for final optimizations**.  
- [ ] Integrate **bonus features if time allows**.  

---

## 🚀 Running the Project  

### **🔹 Prerequisites**  
- **Python 3.x**  
- **stddraw & stdaudio libraries** (No `pygame` or external dependencies).  

### **🔸 How to Run**  
1️⃣ Clone the repository:  
```sh
git clone https://github.com/your-repo/cosmic-conquistadors.git
cd cosmic-conquistadors
```

2️⃣ Run the game:  
```sh
python main.py
```
3️⃣ Controls:  
| Key  | Action |
|------|--------|
| `←` / `→` | Move Shooter Left/Right |
| `A` / `D` | Rotate Turret |
| `Space` | Shoot Missile |
| `Q` | Quit Game |

---

## ⚠️ Important Notes  
❗ **Plagiarism checks will be conducted**, so each section of code must include comments on **who contributed**.  
❗ **The project is tested in FIRGA**, so stick to **allowed libraries**.  
❗ **The April 29 demo is compulsory** – missing it results in **zero marks**.  
