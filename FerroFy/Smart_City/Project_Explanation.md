# 🚦 Project Smart Flow 

## 🌟 Overview

Project Smart Flow Is An Advanced Smart City Traffic Simulation System. It Employs Dual-Mode Capabilities: A Procedural Radar Simulation And An AI-Powered Camera Simulation. The Entire Interface Is Built With HTML, CSS, And JavaScript, Ensuring A Responsive And Visually Engaging Experience.

## 🧠 Core Components

### 1. 🖥️ The User Interface (index.html & Style.css)

The Frontend Is A Modern, Dark-Themed Dashboard Using Bootstrap And Custom CSS. It Features A Live Clock, Simulation Mode Toggles, Real-Time Progress Bars For Lane Occupancy, And A Live Chart Visualizing Traffic Density Over Time.

### 2. ⚙️ The Traffic Engine (Traffic_Engine.js)

This Is The Brain Of The Radar Simulation. It Manages Four Distinct Lanes And Simulates Live Traffic Realities.
- **Traffic Generation** : It Randomly Spawns Different Vehicles (Scooters, Autos, Cars, And Buses) Based On Probability And Weight Values.
- **Apex AI (Anti-Gravity)** : When A Lane Experiences Abnormal Congestion, The System Engages To Rapidly Clear Vehicles By Smoothing Traffic Flow Automatically.
- **Emergency Clearing** : Can Be Triggered To Instantly Empty A Saturated Lane In Case Of An Emergency Vehicle Need.
- **4D Radar** : Detects Hidden Elements Like Small Vehicles To Give Absolute Accuracy Of Live Occupancy.

### 3. 🌉 The Dashboard Logic (Dashboard.js)

This Component Acts As The Bridge Between Our Engine And Visuals. It Creates A Constant Polling Loop That Extracts Information From The Traffic Simulator. It Then Populates Data Log Panels, Animates Traffic Charts, Handles User Inputs Like Flood Or Slider Speed, And Moves Tiny Vehicle Blocks Inside The HTML Container Dynamically.

### 4. 👁️ Neural Vision Processing (Vision_AI.js)

When Put In Camera Simulation Mode, The System Adapts A Real Artificial Intelligence Model (COCO-SSD Using TensorFlow.js) Directly In The Browser.
- **Real-Time Bounding** : Scans Uploaded Traffic Videos Frame By Frame Generating Bounding Boxes Over Target Vehicles.
- **Instant Recognition** : Translates Identified Items Fast. Detects Police Cars Or Ambulances And Interacts Directly With The Core Engine To Fire Off Emergency Signals Instantly!
- **Override Function** : It Overrides Random Number Generations From The Engine And Simply Relays Pure Count Values Extracted From The Neural Feed Processing Into Visual Output.

## 📊 How The Workflow Functions

By Default, It Acts As A Live Radar System Throwing Numbers Predictively. If You Flip The Switch To Camera Mode And Provide A Video, The Mathematics Stop Generatively And Instead The Actual Processed Camera Feed Numbers Update The Screen Metrics! It Keeps Evolving Constantly Ensuring Uninterrupted Monitoring.
