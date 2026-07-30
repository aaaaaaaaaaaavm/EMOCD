# Literature landscape

A map of the field around this project. It is **not** a review, and it must not be read as one.

## Where these came from, and what that is worth

Every entry below is taken from the **reference list of a paper physically in hand**: the five
works analysed in [`PRIOR_ART.md`](PRIOR_ART.md), all of which were read in full. So each citation
is attested by a published, peer-reviewed source that chose to cite it, which is a stronger
provenance than a search result and a weaker one than having read the thing.

The marker after each entry says which of the five cites it:

| | |
|---|---|
| `F` | Feng, Yang & Wu 2025, on-orbit electromagnetic launcher |
| `E` | Einat & Orbach 2023, multi-stage reluctance launcher |
| `Z5` | Zhao et al. 2025, high-volume CubeSat storage device |
| `X` | Xu et al. 2024, in-orbit electromagnetic transfer system |
| `Z2` | Zhao et al. 2022, stacked-CubeSat deployer |

A few carry more than one marker. Those are the papers two independent groups both thought worth
citing, and they are the ones to read first.

## What this file does not claim

**None of the works below has been read.** Bibliographic details are reproduced as the citing paper
printed them, not verified against the publisher record one by one, so a typo in a source paper is
reproduced here. Nothing in this file may support a number in `paper/paper.tex`; that rule is set
in [`RELATED_WORK.md`](RELATED_WORK.md) and it applies with more force here, not less.

Treat it as a reading list with provenance attached. The five works that *have* been read, and the
claims they changed, are in [`PRIOR_ART.md`](PRIOR_ART.md).

## The gap this file exposes

Reference harvesting inherits the biases of the papers harvested. The source set is
coilgun-heavy and deployer-heavy, so the linear-machine and pulsed-power clusters come out thin,
which says more about the sample than the field. Filling those needs a database search, and this
list is the wrong tool for it.


---

## Contents

| Cluster | Entries |
|---|---|
| On-orbit electromagnetic CubeSat launch and transfer | 15 |
| Coilgun and reluctance launchers, with measurements | 25 |
| Railguns, mass drivers and launch to space | 14 |
| Linear machines, magnetics and actuators | 11 |
| Pulsed power, capacitors and drive circuits | 2 |
| CubeSat platforms, missions and standards | 18 |
| Attitude control, vibration and flexible spacecraft | 3 |
| Reachable domain, orbital manoeuvre and pursuit | 10 |
| Robotics, mechanisms and path planning | 8 |
| Unclassified | 30 |
| **Total** | **136** |

---

## On-orbit electromagnetic CubeSat launch and transfer

The cluster this project sits in. Two groups are active in it and both are covered in [`PRIOR_ART.md`](PRIOR_ART.md). What the rest of the cluster shows is that the deployer lineage runs back through the P-POD and the picosatellite dispensers to a spring standard nobody has displaced in twenty years.

- Nason, I.; Puig-Suari, J.; Twiggs, R. Development of a family of picosatellite deployers based on the CubeSat standard. In Proceedings of the IEEE Aerospace Conference, Big Sky, MT, USA, 9–16 March 2002; p. 1 `Z5, X, Z2`
- Johnson, M.D. Satellite Deployer System i.e., CubeSat Deployer for Use in the Field of Space Transportation, Has Ejector Mechanism That Pushes or Pulls Satellite Out of Receptacle, Where Satellite Is Deployed from Launch Vehicle by Ejector Mechanism After Releasable Mechanism Is Released. US2023348116-A1, 2 November 2023 `Z5`
- Xie, C. Research on Design Analysis Method and Key Technology of Star-Arrow Separation Mechanism of Picosatellite. Doctoral Dissertation, Zhejiang University, Hangzhou, China, 2014. (In Chinese) `Z5`
- Zhao, Y.; Yue, H.; Yang, F.; Zhu, J. A High Thrust Density Voice Coil Actuator With a New Structure of Double Magnetic Circuits for CubeSat Deployers. IEEE Trans. Ind. Electron 2022, 69, 13305–13315 `Z5, X, Z2`
- SpaceX. Starlink Multi-Satellite Separation System. Available online: https://www.starlink.com/ (accessed on 20 January 2025) `Z5`
- Heidt, M.; Puig-Suari, J.; Moore, A.S.; Nakasuka, S.; Twiggs, R.J. CubeSat: A New Generation of Picosatellite for Education and Industry Low-Cost Space Experimentation. In Proceedings of the Thirteenth Annual AIAA/USU Small Satellite Conference, Logan, UT, USA, 23–26 August 1999 `X`
- Zhao, Y.; Yue, H.; Mu, X.; Yang, X.; Yang, F. Design and Analysis of a New Deployer for the in Orbit Release of Multiple Stacked CubeSats. Remote Sens. 2022, 14, 4205 `X`
- Jeyakumar, D.; Rao, B.N. Dynamics of Satellite Separation System. J. Sound Vib. 2006, 297, 444–455 `X`
- Liu, X.; Xing, F.; Fan, S.; You, Z. A Compressed and High-Accuracy Star Tracker with On-Orbit Deployable Baffle for Remote Sensing CubeSats. Remote Sens. 2021, 13, 2503 `Z2`
- Heidt, M.H.; Puig-Suari, P.J.; Augustus, P.; Nakasuka, S.; Twiggs, R. CubeSat: A new generation of picosatellite for education and industry low-cost space experimentation. In Proceedings of the Thirteenth Annual AIAA/USU Small Satellite Conference, Logan, Utah, 21–24 August 2000 `Z2`
- Hevner, R. Lessons learned flight validating an innovative Canisterized Satellite Dispenser. In Proceedings of the IEEE Aerospace Conference, Big Sky, MT, USA, 1–8 May 2014; pp. 1–14 `Z2`
- Zhao, X.; Zhao, C.; Li, J.; Guan, Y.; Chen, S.; Zhang, L. Research on Design, Simulation, and Experiment of Separation Mechanism for Micro-Nano Satellites. Appl. Sci. 2022, 12, 5997 `Z2`
- Heidt, H.; Suari, J.P.; Moore, A.S.; Nakasuka, S.; Twiggs, R.J. CubeSat: A new generation of picosatellite for education and industry low-cost space experimentation. In Proceedings of the Fourteenth Annual AIAA/USU Small Satellite Conference, Berlin, Germany, 2–6 April 2001; pp. 1–19 `Z2`
- Jordi, P.S.; Turner, C.; Ahlgren, W. Development of the Standard CubeSat Deployer and a CubeSat Class PicoSatellite. In Proceedings of the Aerospace Conference, Big Sky, MT, USA, 10–17 March 2001; Volume 1, pp. 347–353 `Z2`
- Xie, C.X. Research on Design Analysis Method and Key Technologies of Pico-Satellite Separation Mechanism; Zhejiang University: Hangzhou, China, 2014 `Z2`

---

## Coilgun and reluctance launchers, with measurements

The largest cluster, and the one carrying most of the field's measured results. Almost all of it operates below a kilogram. Einat and Orbach's own survey is the useful entry point: it collects launch velocity and energy for five years of experiments, and the pattern is that velocity and projectile mass trade against each other hard. ADR-003 rejected this branch, and these are the papers that would have to be wrong for that to be the wrong call.

- T. R. Lockner, R. J. Kaye, and B. N. Turman, "Coilgun Technology, Status, Applications and Future Directions at Sandia National Laboratories," in Conference Record of the TwentySixth International Power Modulator Symposium, 2004 and 2004 High-Voltage Workshop (San Francisco, CA, USA: IEEE, 2004), doi:10.1109/MODSYM.2004.1433521 `F`
- R. Ram and M. J. Thomas, "Study on the Performance of the Sleeve Projectiles of Different Materials and Dimensions Launched Using a Four-Stage Induction Coilgun," IEEE Transactions on Plasma Science 51, no. 10 (2023): 2885– 2893, doi:10.1109/TPS.2023.3297668 `F`
- K. A. Polzin, A. Cipriano, A. K. Martin, and C. Liu, "Coilgun Acceleration Model Containing Multiple Interacting Coils," in Forum, American Institute of Aeronautics and Astronautics (AIAA Scitech, 2019), doi:10.2514/6.2019-1247 `F`
- M. U. Manzoor, H. Asif, Shoaib-Ur-Rehman, and T. Abbas, "Split Coil Based Design of a Coilgun," in 2017 13th International Conference on Emerging Technologies (ICET) (Islamabad, Pakistan: IEEE, 2017), doi:10.1109/ ICET.2017.8281739 `F`
- R. Ram and M. J. Thomas, "Experimental and Computational Studies on the Eﬃciency of an Induction Coilgun," IEEE Transactions on Plasma Science 48, no. 10 (2020): 3392– 3400, doi:10.1109/TPS.2020.3007551 `F`
- J. T. Camp, "Optimizing Coilgun Geometry to Maximize Eﬃciency," IEEE Transactions on Plasma Science 50, no. 10 (2022): 3816–3823, doi:10.1109/TPS.2022.3201687 `F`
- M.-G. Song, Y. Lee, H. M. Kim, et al., "Development and Experimental Results of a Three-Stage Induction Coilgun," IEEE Transactions on Plasma Science 47, no. 5 (2019): 2438– 2444, doi:10.1109/TPS.2018.2887116 `F`
- M.-G. Song, Y. Lee, H. M. Kim, et al., "Design, Fabrication, and Experimental Results of a Pulsed Power-Based Four-Stage Induction Coilgun for Launching a Heavy Projectile," IEEE Transactions on Plasma Science 49, no. 9 (2021): 2916–2924, doi:10.1109/TPS.2021.3103018 `F`
- M. Baharvand, A. D. Kolagar, and M. R. A. Pahlavani, "Design, Simulation, and Parameter Optimization of a MultiStage Induction Coilgun System," IEEE Transactions on Plasma Science 49, no. 7 (2021): 2256–2264, doi:10.1109/ TPS.2021.3085775 `F`
- Xiang, H., Lei, B., Li, Z. & Zhao, K. Design and experiment of reluctance electromagnetic launcher with new-style armature. IEEE Trans. Plasma Sci. 41(5), 1066–1069 (2013) `E`
- Kim, J. & Ahn, J. Modeling and optimization of a reluctance accelerator using DOE-based response surface methodology. J. Mech. Sci. Technol. 31(3), 1321–1330 (2017) `E`
- Manzoor, M. U., Asif, H. & Abbas, T. Split coil based design of a coilgun. In 2017 13th International Conference on Emerging Technologies (ICET) (2017) `E`
- Zhu, B., Lu, J., Wang, J. & Xiong, S. A compulsator driven reluctance coilgun-type electromagnetic launcher. IEEE Trans. Plasma Sci. 45(9), 2511–2518 (2017) `E`
- Gies, V., Soriano, T., Albert, C. & Prouteau, N. Modelling and optimisation of a RoboCup MSL Coilgun. In RoboCup 2019: Robot World Cup XXIII. RoboCup 2019. Lecture Notes in Computer Science Vol. 11531 (eds Chalup, S. et al.) (Springer, Cham, 2019) `E`
- Rivas-Camacho, J. L., Ponce-Silva, M. & Olivares-Peregrino, V. H. The ringer as an inductive power source for a reluctance accelerator. IEEE Trans. Plasma Sci. 47(5), 2275–2281 (2019) `E`
- Orbach, Y., Oren, M., Golan, A. & Einat, M. Reluctance launcher coil-gun simulations and experiment. IEEE Trans. Plasma Sci. 47(2), 1358–1363 (2019) `E`
- Gies, V. et al. Optimisation of energy transfer in reluctance coil guns: Application to soccer ball launchers. Appl. Sci. 10(9), 3137 (2020) `E`
- Deng, H. M., Wang, Y., Lu, F. L. & Yan, Z. M. Optimization of reluctance accelerator efficiency by an improved discharging circuit. Def. Technol. 16(3), 662–667 (2020) `E`
- Coramik, M. et al. Studies to increase barrel exit velocity for four-stage coil-gun. IEEE Trans. Plasma Sci. 48(7), 2618–2627 (2020) `E`
- Dındış, G. Lagrangian description and finite element analysis of reluctance accelerator circuit model. ESOGÜ Müh. Mim. Fak. Derg. 28(2), 94–106 (2020) `E`
- Deng, H. M., Wang, Y. & Yan, Z. M. Study on the influence of armature on the efficiency of reluctance accelerator. Def. Technol. doi:10.1016/j.dt.2021.01.003 (2021) `E`
- Hassannia, A. & Abedi, K. Optimal switching scheme for multistage reluctance coilgun. IEEE Trans. Plasma Sci. 49(3), 1241–1246 (2021) `E`
- Orbach, Y., Oren, M. & Einat, M. 75 m/s simulation and experiment of two-stage reluctance coilgun. J. Mech. Sci. Technol. 36(3), 1123–1130 (2022) `E`
- Zhao, Y.; Yue, H.; Zhu, J.G.; Yang, F. Armature Reaction Analysis and Suppression of Voice Coil Actuator Based on an Improved Magnetic Equivalent Circuit Model. IEEE Trans. Ind. Electron. 2024, 71, 7599–7609 `Z5`
- Zhao, Y.; Yue, H.; Zhu, J.; Yang, F. Armature Reaction Analysis and Suppression of Voice Coil Actuator Based on an Improved Magnetic Equivalent Circuit Model. IEEE Trans. Ind. Electron. 2023, 71, 7599–7609 `X`

---

## Railguns, mass drivers and launch to space

Ground-to-orbit and lunar launch. Recorded to mark the boundary rather than because it informs the design: those systems run at accelerations three orders above anything a CubeSat survives, and their relevance here is limited to pulsed power and thermal management, where the engineering does transfer.

- "Japan Looks to Partner with U.S. on Railgun Project," Retrieved 13 April 2025. https://www .nationaldefensemagazine.org/articles/2023/4/17/japanlooks-to-partner-with-us-on-railgun-project `F`
- Gibney, E. How to build a Moon base. Nature 562(7728), 474–478 (2018) `E`
- Gibney, E. Asteroids, Hubble rival and Moon base: China sets out space agenda. Nature 603(7899), 19–20 (2022) `E`
- Kornuta, D. et al. Commercial lunar propellant architecture: A collaborative study of lunar propellant production. Reach 13, 100026 (2019) `E`
- Ní Chúláin, A. Paving the way to Mars by producing oxygen from soil on the Moon. euronews.com (2021) `E`
- Mascolo, L. & Stoica, A. Electro-magnetic launchers on the moon: A feasibility study. In 2018 NASA/ESA Conference on Adaptive Hardware and Systems (AHS). IEEE (2018) `E`
- Inger, E. Electromagnetic launching systems to geosynchronously equatorial orbit in space and cost calculations. IEEE Trans. Plasma Sci. 45(7), 1663–1666 (2017) `E`
- Inger, E. Mass driver design traveling Earth to the Moon. IEEE Access 7, 161034–161039 (2019) `E`
- McNab, I. R. Launch to space with an electromagnetic railgun. IEEE Trans. Magn. 39(1), 295–304 (2003) `E`
- McNab, I. R. A lunar astronaut launcher. IEEE Trans. Plasma Sci. 48(11), 4014–4020 (2020) `E`
- Bolonkin, A. & Krinker, M. Railgun space launcher. J. Aerosp. Eng. 23(4), 293–299 (2010) `E`
- Kutter, B.F.; Sowers, G.F.; Cislunar, F. Transportation supporting a self-sustaining space economy. In Proceedings of the AIAA SPACE 2016, Long Beach, CA, USA, 13–16 September 2016 `Z5`
- Zielinski, A.E.; Delguercio, M.A. Analytical study of the injection of a moving projetile into a railgun. IEEE Trans. Plasma Sci. 2011, 39, 235–240 `Z5`
- Nosseir, A.E.S.; Cervone, A.; Pasini, A. Modular Impulsive Green Monopropellant Propulsion System (MIMPS-G): For CubeSats in LEO and to the Moon. Aerospace 2021, 8, 169 `Z2`

---

## Linear machines, magnetics and actuators

The topology this design uses. Thinner than it should be, because the source papers are coilgun-oriented and cite comparatively little linear-machine literature. This is the cluster most in need of a proper database search rather than reference harvesting.

- "European Partners Launch THEMA Consortium for Advanced Electromagnetic Artillery System," Retrieved 13 April 2025. https://www.defensemirror.com/news/36153/ `F`
- Wright, M. R., Kuznetsov, S. B. & Kloesel, K. J. A lunar electromagnetic launch system for in situ resource utilization. IEEE Trans. Plasma Sci. 39(1), 521–528 (2010) `E`
- Engel, T. G. & Prelas, M. A. Asteroid mining and deflection using electromagnetic launchers. IEEE Trans. Plasma Sci. 45(7), 1327–1332 (2017) `E`
- Makowski, T. & Kluszczyński, K. Dynamic model of hybrid electromagnetic launcher for simulations in LabVIEW environment. In 2017 International Symposium on Electrical Machines (SME) (2017) `E`
- Castillo, J., Gama, N. & Amaya, D. Projectile accelerator prototype using electromagnetic fields. Res. J. Appl. Sci. 13(1), 59–66 (2018) `E`
- Citak, H., Ege, Y. & Coramik, M. Design and optimization of Delphi-based electromagnetic coilgun. IEEE Trans. Plasma Sci. 47(5), 2186–2196 (2019) `E`
- Kim, S. & Kim, J. Optimal design of a coil gun projectile by analyzing the drag coefficient and electromagnetic force on the projectile. J. Mech. Sci. Technol. 34, 2903–2911 (2020) `E`
- Zhao, Y.; Yue, H.; Zhu, J.G.; Yang, X.Z. A Planar Electromagnetic Actuator With Passive Adsorption for CubeSats Transport in a Weightless Environment. IEEE Trans. Ind. Electron. 2023, 70, 10396–10407 `Z5`
- Zhao, Y.; Yue, H.; Zhu, J.; Yang, X. A Planar Electromagnetic Actuator With Passive Adsorption for CubeSats Transport in a Weightless Environment. IEEE Trans. Ind. Electron. 2023, 70, 10396–10408 `X`
- Zhu, H.; Teo, T.J.; Pang, C.K. Design and Modeling of a Six-Degree-of-Freedom Magnetically Levitated Positioner Using Square Coils and 1-D Halbach Arrays. IEEE Trans. Ind. Electron. 2017, 64, 440–450 `Z2`
- Glushchenkov, V.A.; Yusupov, R.Y. Controlled separation of nanosatellites by means of the pulsed magnetic field. Russ. Aeronaut 2017, 60, 1–8 `Z2`

---

## Pulsed power, capacitors and drive circuits

Two entries, which understates the field badly and reflects how the list was built rather than what exists. A8 validated the pulse chain against ngspice and would benefit from more here.

- Kim, S. & Kim, J. Control of discharge time using physical contact in a two-stage coil gun. Adv. Mech. Eng. 11(9), 1–8 (2019) `E`
- Akay, C., Bavuk, U., Tunçdamar, A. & Özer, M. Coilgun design and evaluation without capacitor. J. Mechatron. Artif. Intell. Eng. 1(2), 53–62 (2020) `E`

---

## CubeSat platforms, missions and standards

Context rather than method: what CubeSats are for, how many fly, and which standards bound the mechanical interface. The CubeSat Design Specification and the NASA small-spacecraft state-of-the-art volume are the two that constrain this design directly.

- S. V. Weston, C. D. Burkhard, J. M. Stupl, et al., State-of-theArt Small Spacecraft Technology (NASA, 2025) `F`
- "10.0 Integration, Launch, and Deployment – NASA," Retrieved 4 October 2025, https://www.nasa.gov/smallsatinstitute/sst-soa/integration-launch-and-deployment/ `F`
- L. Maciulis and V. Buzas, "LituanicaSAT-2: Design of the 3U in-Orbit Technology Demonstration CubeSat," IEEE Aerospace and Electronic Systems Magazine 32, no. 6 (2017): 34– 45, doi:10.1109/MAES.2017.150245 `F`
- Lombardo, M.; Zannoni, M.; Gai, I.; Casajus, L.G.; Gramigna, E.; Manghi, R.L.; Tortora, P.; Di Tana, V.; Cotugno, B.; Simonetti, S.; et al. Design and analysis of the cis-lunar navigation for the Argo moon CubeSat mission. Aerospace 2022, 9, 659 `Z5`
- Bouwmeester, J.; Guo, J. Survey of worldwide pico- and nanosatellite missions, distributions and subsystem technology. Acta Astronaut 2010, 67, 854–862 `Z5`
- Dobrowolski, M.; Grygorczuk, J.; Kedziora, B.; Tokarz, M.; Borys, M. Dragon—8u nanosatellite orbital deployer. In Proceedings of the 42nd Aerospace Mechanisms Symposium, Baltimore, MD, USA, 14–16 May 2014; pp. 1–10 `Z5, X`
- Pranajaya, F.M.; Zee, R.E. The generic nanosatellite bus: From space astronomy to formation flying demo to responsive space. In Proceedings of the International Conference on Advances in Satellite and Space Communications, Siena-Tuscany, Italy, 10–11 September 2009; pp. 134–140 `Z5, X, Z2`
- Brezovnik, S.; Gotlih, J.; Balič, J.; Gotlih, K.; Brezočnik, M. Optimization of an automated storage and retrieval systems by swarm intelligence. Procedia Eng. 2015, 100, 1309–1318 `Z5`
- Liu, S.; Theoharis, P.I.; Raad, R.; Tubbal, F.; Theoharis, A.; Iranmanesh, S.; Abulgasem, S.; Khan, M.U.A.; Matekovits, L. A Survey on CubeSat Missions and Their Antenna Designs. Electronics 2022, 11, 2021 `X, Z2`
- Fernandez, L.; Sobrino, M.; Ruiz-de-Azua, J.A.; Calveras, A.; Camps, A. Design of a Deployable Helix Antenna at L-Band for a 1-Unit CubeSat: From Theoretical Analysis to Flight Model Results. Sensors 2022, 22, 3633 `X, Z2`
- Azami, M.H.b.; Orger, N.C.; Schulz, V.H.; Oshiro, T.; Cho, M. Earth Observation Mission of a 6U CubeSat with a 5-Meter Resolution for Wildfire Image Classification Using Convolution Neural Network Approach. Remote Sens. 2022, 14, 1874 `X, Z2`
- Bernal, C.A.; van Bolhuis, M. Releasing the Cloud: A Deployment System Design for the QB50 CubeSat Mission. In Proceedings of the Small Satellite Conference, Logan, UT, USA, 14 August 2012; p. 1 `X`
- Bogomolov, A.V.; Bogomolov, V.V.; Iyudin, A.F.; Eremeev, V.E.; Kalegaev, V.V.; Myagkova, I.N.; Osedlo, V.I.; Petrov, V.L.; Peretjat'ko, O.Y.; Prokhorov, M.I.; et al. Space Weather Effects from Observations by Moscow University Cubesat Constellation. Universe 2022, 8, 282 `Z2`
- Pellegrino, A.; Pancalli, M.G.; Gianfermo, A.; Marzioli, P.; Curianò, F.; Angeletti, F.; Piergentili, F.; Santoni, F. HORUS: Multispectral and Multiangle CubeSat Mission Targeting Sub-Kilometer Remote Sensing Applications. Remote Sens. 2021, 13, 2399 `Z2`
- Dobrowolski, M.; Tokarz, M.; Borys, M. DRAGON—8U Nanosatellite Orbital Deployer. In Proceedings of the 42nd Aerospace Mechanisms Symposium, Baltimore, MD, USA, 14–16 May 2014 `Z2`
- Pranajaya, F.M.; Zee, R.E. Generic Nanosatellite Bus for Responsive Mission. In Proceedings of the 5th Responsive Space Conference, Los Angeles, CA, USA, 23–26 April 2007. Remote Sens. 2022, 14, 4205 20 of 20 `Z2`
- Belokonov, I.V.; Timbai, I.A.; Nikolaev, P.N. Analysis and Synthesis of Motion of Aerodynamically Stabilized Nanosatellites of the CubeSat Design. Gyroscopy Navig. 2018, 9, 287–300 `Z2`
- Filonin, O.V.; Belokonov, I.V.; Gimranov, Z.I. Small-Size Automatic System for the Controllable Launch of Nanosatellites on a Desired Trajectory. Russ. Aeronaut. 2019, 62, 184–191 `Z2`

---

## Attitude control, vibration and flexible spacecraft

Relevant through E24. Moving mass inside a deployer disturbs the platform it is mounted on, and this is the literature that treats that as a control problem rather than a nuisance.

- B. Lyu, X. Yue, and C. Liu, "Parallel Layered Scheme-Based Integrated Orbit-Attitude-Vibration Coupled Dynamics and Control for Large-Scale Spacecraft," ISA Transactions 158 (2025): 415–426, doi:10.1016/j.isatra.2024.12.033 `F`
- B. Lyu, C. Liu, and X. Yue, "Integrated Predictor–Observer Feedback Control for Vibration Mitigation of Large-Scale Spacecraft With Unbounded Input Time Delay," IEEE Transactions on Aerospace and Electronic Systems 61, no. 2 (2025): 4561–4572, doi:10.1109/TAES.2024.3505851 `F`
- C. Liu, X. Yue, J. Zhang, and K. Shi, "Active Disturbance Rejection Control for Delayed Electromagnetic Docking of Spacecraft in Elliptical Orbits," IEEE Transactions on Aerospace and Electronic Systems 58, no. 3 (2022): 2257–2268, https:// doi.org/10.1109/TAES.2021.3130830 `F`

---

## Reachable domain, orbital manoeuvre and pursuit

The method Feng et al. apply, and the one this project should adopt in place of a scalar lifetime multiplier. Ten entries here give the formulation a real grounding, including the alpha-shape work that makes the envelope computable.

- S. Zhang, Z. Yang, and Y.-Z. Luo, "Time-Dependent Reachable Domain and Its Application to Impulsive Orbital Pursuit–Evasion Analysis," Journal of Spacecraft and Rockets 62, no. 2 (2025): 631–642, doi:10.2514/1.A36112 `F`
- Z. H. Sai, Y. A. Zhen, and L. U. Yazhong, "An Algorithm for Solving Spacecraft Reachable Domain With Single-Impulse Maneuvering in ECEF Coordinate System," MECHANICS in Engineering 44, no. 6 (2022): 1286–1296, https://doi.org/ 10.6052/1000-0879-22-265 `F`
- L. Xuehua, H. Xingsuo, Z. Qinfang, and S. Ming, "Reachable Domain for Satellite With Two Kinds of Thrust," Acta Astronautica 68, no. 11-12 (2011): 1860–1864, https://doi.org/ 10.1016/j.actaastro.2011.01.004 `F`
- C. Xia, G. Zhang, and Y. Geng, "Reachable Domain With a Single Coplanar Impulse Considering the Target-Visit Constraint," Advances in Space Research 69, no. 10 (2022): 3847– 3855, doi:10.1016/j.asr.2022.02.042 `F`
- L. Lu, J. Zhou, H. Li, and H. Zhang, "Investigation on Reachable Domain of Contingency Return Trajectories in the Circumlunar Flight Phase Based on Interval Analysis," Advances in Space Research 72, no. 9 (2023): 3770–3786, https:// doi.org/10.1016/j.asr.2023.07.023 `F`
- C. Wen and P. Gurfil, "Relative Reachable Domain for Spacecraft With Initial State Uncertainties," Journal of Guidance, Control, and Dynamics 39, no. 3 (2016): 462–473, https:// doi.org/10.2514/1.G000721 `F`
- X. Cao, X. Ning, S. Liu, et al., "Spacecraft Intelligent Orbital Game Technology: A Review," Chinese Journal of Aeronautics 38, no. 6 (2025): 103480, doi:10.1016/ j.cja.2025.103480 `F`
- P. Sun, S. Li, M. Trisolini, and C. Colombo, "A Multi-Segment Alpha Shape-Based Continuum Method for Long-Term Density Propagation With Bifurcation," Nonlinear Dynamics 112, no. 5 (2024): 3481–3503, doi:10.1007/s11071-02309186-z `F`
- Q. Chen, D. Qiao, H. Shang, and X. Liu, "A New Method for Solving Reachable Domain of Spacecraft With a Single Impulse," Acta Astronautica 145 (2018): 153–164, https:// doi.org/10.1016/j.actaastro.2018.01.040 `F`
- Z. Liao, J. Liu, G. Shi, and J. Meng, "Grid Partition Variable Step Alpha Shapes Algorithm," Mathematical Problems in Engineering 2021 (2021): 9919003, doi:10.1155/ 2021/9919003 `F`

---

## Robotics, mechanisms and path planning

Drawn in by the Harbin group, who treat magazine indexing as a planning problem. Peripheral to a single-track deployer, and directly relevant if the magazine ever grows past two cassettes.

- Tang, G.; Tang, C.; Claramunt, C.; Hu, X.; Zhou, P. Geometric A-Star Algorithm: An Improved A-Star Algorithm for AGV Path Planning in a Port Environment. IEEE Access 2021, 9, 59196–59210 `X`
- Han, C.; Li, B. Mobile Robot Path Planning Based on Improved A* Algorithm. In Proceedings of the 2023 IEEE 11th Joint International Information Technology and Artificial Intelligence Conference (ITAIC), Chongqing, China, 8–10 December 2023; pp. 672–676 `X`
- Wang, H.; Lou, S.; Jing, J.; Wang, Y.; Liu, W.; Liu, T. The EBS-A* Algorithm: An Improved A* Algorithm for Path Planning. PLoS ONE 2022, 17, e0263841 `X`
- Liu, C.; Mao, Q.; Chu, X.; Xie, S. An Improved A-Star Algorithm Considering Water Current, Traffic Separation and Berthing for Vessel Path Planning. Appl. Sci. 2019, 9, 1057 `X`
- Fan, G.; Xing, X.; Han, Y.; Chen, M.; Gui, H. Path Planning for Ground Target Reconnaissance Based on Improved Astar Algorithm. In Proceedings of the 2021 China Automation Congress (CAC), Beijing, China, 22–24 October 2021; pp. 2092–2097 `X`
- Fan, Y.; Deng, F.; Shi, X. Multi-Robot Task Allocation and Path Planning System Design. In Proceedings of the 2020 39th Chinese Control Conference (CCC), Shenyang, China, 27–29 July 2020; pp. 4759–4764 `X`
- Li, M.; Qiao, L.; Jiang, J. A Multigoal Path-Planning Approach for Explosive Ordnance Disposal Robots Based on Bidirectional Dynamic Weighted-A* and Learn Memory-Swap Sequence PSO Algorithm. Symmetry 2023, 15, 1052 `X`
- Ou, Y.; Fan, Y.; Zhang, X.; Lin, Y.; Yang, W. Improved A* Path Planning Method Based on the Grid Map. Sensors 2022, 22, 6198 `X`

---

## Unclassified

Everything the keyword pass could not place. Mostly CubeSat mission context and a few textbook and news items. Left visible rather than force-fitted into a cluster.

- S. Chaumette and J. Ouoba, Cubesat Design Specification (2014doi:10.4108/icst.mobicase.2014.258028 `F`
- Nikitaev, D. & Thomas, L. D. Preliminary results for in-situ alternative propellants for nuclear thermal propulsion. Nucl. Technol. doi:10.1080/00295450.2021.2021768 (2022) `E`
- Witze, A. Revealed: How a spacecraft will bring Mars rocks to Earth. Nature doi:10.1038/d41586-020-01114-0 (2020) `E`
- Meinel, C. For love of a gun. IEEE Spectr. 44(7), 40–46 (2007) `E`
- Purcell, E. M. & Morin, D. J. Electricity and Magnetism 3rd edn, 523–575 (Cambridge University Press, 2013) `E`
- Bao, W.M.; Wang, X.W. Develop high reliable and low-cost technology of access to space, embrace new space economy era. China Aerosp. 2019, 20, 23–30 `Z5`
- Poghosyan, A.; Golkar, A. CubeSat evolution: Analyzing CubeSat capabilities for conducting science missions. Prog. Aerosp. Sci. 2017, 1, 59–83 `Z5`
- Saeed, N.; Elzanaty, A.; Almorad, H.; Dahrouj, H.; Al-Naffouri, T.Y.; Alouini, M.-S. CubeSat communications: Recent advances and future challenges. IEEE Commun. Surv. Tutor. 2020, 22, 1839–1862 `Z5`
- Toorian, A.; Diaz, K.; Lee, S. The CubeSat approach to space access. In Proceedings of the IEEE Aerospace Conference, Big Sky, MT, USA, 1–8 March 2008; Volume 5, pp. 1–14 `Z5`
- Mohamed, R. Design and Implementation of Ground Support Equipment for Characterizing Performance of XPOD and CNAPS & Thermal Analysis of CNAPS Pressure Regulator Valve. Ph.D. Thesis, University of Toronto, Toronto, ON, Canada, 2009 `Z5, X`
- Wu, H.; Wang, D.; Zhang, X.; Zhao, C.; Wang, D. Development and inspiration of the Dutch space innovation solutions company. Space Ind. Manag. 2018, 408, 52–56. (In Chinese) `Z5`
- Launch Services for Small Satellites and CubeSats. Available online: https://www.exolaunch.com/ (accessed on 5 May 2025) `Z5`
- Gue, K.R. Very high density storage systems. IIE Trans. 2006, 38, 79–90 `Z5`
- Li, F.; Niu, D.; Li, T.; Xue, Y.; Huang, X. Research and design of cloud monitoring and management system for intelligent stereo garage. J. Eng. 2019, 22, 8335–8338 `Z5`
- Nils, B.; Konrad, S. A survey on single crane scheduling in automated storage/retrieval systems. Eur. J. Oper. Res. 2016, 254, 691–704 `Z5`
- Carlo, H.J.; Iris, F.A.; Vis, B. Sequencing dynamic storage systems with multiple lifts and shuttles. Int. J. Prod. Econ. 2012, 140, 844–853 `Z5`
- Ekren, B.Y.; Heragu, S.S. Simulation based performance analysis of an autonomous vehicle storage and retrieval system. Simul. Model. Pract. Theory 2011, 19, 1640–1650 `Z5`
- Kallo, N.; Koltai, T. Increasing customer satisfaction in queuing systems with rapid modelling. In Rapid Modelling and Quick Response; Springer Nature: London, UK, 2010; pp. 119–130. Aerospace 2025, 12, 466 31 of 31 `Z5`
- Puig-Suari, J.; Turner, C.; Twiggs, R.J. CubeSat: The Development and Launch Support Infrastructure for Eighteen Different Satellite Customers on One Launch. In Proceedings of the 15th Annual AIAA/USU Conference on Small Satellites, Logan, UT, USA, 13–16 August 2001 `X`
- Lee, S.; Toorian, A.; Clemens, N.; Puig-Suari, J.; Twiggs, B. Cal Poly Coordination of Multiple CubeSats on the DNEPR Launch Vehicle. In Proceedings of the 18th Annual AIAA/USU Conference on Small Satellites, Carefree, AZ, USA, 9–11 August 2004 `X`
- Thompson, L.D. Development of a NASA 6-U Satellite. In Proceedings of the Small Satellite Conference, Logan, UT, USA, 8–11 August 2011; p. 1 `X`
- Akagi, H.; Takata, M.; Watanabe, H.; Sano, T.; Oikawa, K. Kibo's Contribution to Broadening the Possibilities for Micro/Nano- Satellite. In Proceedings of the SpaceOps Conferences, Daejeon, Korea, 16–20 May 2016; pp. 1–10 `X`
- Kılıç, Ç.; Scholz, T.; Asma, C. Deployment Strategy Study of QB50 Network of CubeSats. In Proceedings of the 6th International Conference on Recent Advances in Space Technologies (RAST), Istanbul, Turkey, 12–14 June 2013; pp. 935–939 `X`
- Lee, S.; Clemens, N.; Puig-Suari, J.; Twiggs, B. Cal Poly Coordination of Multiple CubeSats on the DNEPR Launch Vehicle. In Proceedings of the 18th Annual AIAA/USU Conference on Small Satellites, Carefree, AZ, USA, 9–11 August 2004 `Z2`
- Ashida, H.; Fujihashi, K.; Inagawa, S.; Miura, Y.; Omagari, K.; Miyashita, N.; Matunaga, S.; Toizumi, T.; Kataoka, J.; Kawai, N.; et al. Design of Tokyo Tech nano-satellite Cute-1.7+APD II and its operation. Acta Astronaut. 2010, 66, 1412–1424 `Z2`
- Akagi, H.; Takata, M.; Watanabe, H.; Oikawa, K. Kibo's contribution to broadening the possibilities for Micro/Nano-Satellite. In Proceedings of the SpaceOps 2016 Conferences, Daejeo, Korea, 16–20 May 2016; pp. 1–8 `Z2`
- Ali, M.R. Design and Implementation of Ground Support Equipment for Characterizing Performance of XPOD and CNAPS & Thermal Analysis of CNAPS Pressure Regulator Valve; University of Toronto: Toronto, ON, Canada, 2009 `Z2`
- Fujihashi, K.; Omagari, K.; Fujiwara, K.; Konda, Y.; Maeno, M.; Tanaka, Y.; Ueno, T.; Ashida, H.; Nishida, J.; Hagiwara, Y.; et al. Development of Tokyo Tech Nano-Satellite Cute-1.7+APD II. In Proceedings of the 17th Workshop on JAXA Astrodynamics and Flight Mechanics, Sagamihara, Japan, 28 March 2007; Volume 107, pp. 33–38 `Z2`
- Zhang, C.; Huang, X.; Yang, M.; Chen, S.; Yang, G. Design of a Long Stroke Nanopositioning Stage with Self-Damping Actuator and Flexure Guide. IEEE Trans. Ind. Electron. 2022, 69, 10417–10427 `Z2`
- Zhang, Z.; Luo, M.; Zhou, H.; Duan, J.-A. Design and Analysis of a Novel Two-Degree-of-Freedom Voice Coil Motor. IEEE/ASME Trans. Mechatron. 2019, 24, 2908–2918 `Z2`
