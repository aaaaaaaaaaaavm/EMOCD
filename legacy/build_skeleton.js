const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, PageBreak,
  Table, TableRow, TableCell, WidthType, ImageRun, Footer, PageNumber, NumberFormat,
  TableOfContents, SectionType, BorderStyle, LineRuleType } = require('docx');

const manifest = JSON.parse(fs.readFileSync('figs/manifest.json'));
const MARGIN = 1417; // 2.5 cm in twips

// ---------- helpers ----------
const T = (text, opts={}) => new TextRun(Object.assign({ text, font: 'Times New Roman' }, opts));
const P = (children, opts={}) => new Paragraph(Object.assign({ children: Array.isArray(children)?children:[children] }, opts));
const center = { alignment: AlignmentType.CENTER };
const blank = () => new Paragraph({ text: '' });
const pageBreak = () => new Paragraph({ children: [new PageBreak()] });

function scaffold(note){ // bracketed drafting note, italic gray
  return P(T('[To draft: ' + note + ']', { italics: true, color: '808080', size: 22 }));
}
function placeholder(note){
  return new Paragraph({ alignment: AlignmentType.CENTER, spacing:{before:120,after:120},
    border: { top:{style:BorderStyle.DASHED,size:6,color:'999999'}, bottom:{style:BorderStyle.DASHED,size:6,color:'999999'},
              left:{style:BorderStyle.DASHED,size:6,color:'999999'}, right:{style:BorderStyle.DASHED,size:6,color:'999999'} },
    children: [T('[ PLACEHOLDER — ' + note + ' ]', { italics: true, color: '666666' })] });
}
function fig(file, caption, widthPx=460){
  const [w,h] = manifest[file];
  const height = Math.round(widthPx*h/w);
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, spacing:{line:240,lineRule:LineRuleType.AUTO}, children: [ new ImageRun({ data: fs.readFileSync('figs96/'+file), type:'png', transformation:{ width: widthPx, height } }) ] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing:{after:200,line:240,lineRule:LineRuleType.AUTO}, children: [T(caption, { size: 20 })] })
  ];
}
function row(cells, widths){
  return new TableRow({ children: cells.map((c,i)=> new TableCell({ width:{size:widths[i],type:WidthType.DXA},
    children:[ new Paragraph({ spacing:{line:240,lineRule:LineRuleType.AUTO}, children:[T(c,{size:22})] }) ] })) });
}
function simpleTable(rows, widths){
  return new Table({ columnWidths: widths, width:{size:widths.reduce((a,b)=>a+b,0), type:WidthType.DXA},
    rows: rows.map(r=>row(r,widths)) });
}

// ---------- front matter section (roman numerals) ----------
const front = [];

// Title page
front.push(blank(), blank(),
  P(T('A PROJECT BASED LEARNING-II REPORT ON', { bold:true, size:28 }), center), blank(),
  P(T('DESIGN AND ANALYSIS OF AN ELECTROMAGNETIC LINEAR-MOTOR DEPLOYMENT SYSTEM FOR CUBESAT RIDESHARE MISSIONS', { bold:true, size:32 }), center), blank(),
  P(T('SUBMITTED IN PARTIAL FULFILLMENT OF THE REQUIREMENT FOR THE AWARD OF THE DEGREE OF', { size:28 }), center), blank(),
  P(T('BACHELOR OF TECHNOLOGY', { bold:true, size:28 }), center),
  P(T('IN', { bold:true, size:28 }), center),
  P(T('MECHANICAL ENGINEERING', { bold:true, size:28 }), center), blank(),
  P(T('SUBMITTED BY', { bold:true, size:24 }), center), blank(),
  P(T('[STUDENT 1 NAME — REGISTRATION NO.]', { bold:true, size:32 }), center),
  P(T('[STUDENT 2 NAME — REGISTRATION NO.]', { bold:true, size:32 }), center), blank(),
  P(T('Under the Guidance of', { bold:true, size:24 }), center),
  P(T('[GUIDE NAME AND TITLE]', { bold:true, size:28 }), center), blank(),
  P(T('SYMBIOSIS INSTITUTE OF TECHNOLOGY', { bold:true, size:24 }), center),
  P(T('A CONSTITUENT OF SYMBIOSIS INTERNATIONAL (DEEMED UNIVERSITY)', { bold:true, size:24 }), center),
  P(T('Pune – 412115', { bold:true, size:24 }), center),
  P(T('2026', { bold:true, size:24 }), center),
  pageBreak());

// Inside cover = same as title
front.push(P(T('[INSIDE COVER — duplicate of title page; copy after names are final]', { italics:true, color:'808080' }), center), pageBreak());

// Certificate
front.push(P(T('(Annexure 2)', { bold:true }), { alignment: AlignmentType.RIGHT }),
  P(T('CERTIFICATE', { bold:true, size:28 }), center), blank(),
  P([T('The report titled '), T('Design and Analysis of an Electromagnetic Linear-Motor Deployment System for CubeSat Rideshare Missions', { italics:true }),
     T(' submitted to the Symbiosis Institute of Technology, Pune for the award of B. Tech in Mechanical Engineering is based on our original work carried out under the guidance of [GUIDE NAME]. The report has not been submitted elsewhere for award of any degree.')]),
  P(T('The material borrowed from other sources and incorporated in the report has been duly acknowledged and/or referenced.')),
  P(T('We understand that we ourselves could be held responsible and accountable for plagiarism, if any, detected later on.')), blank(),
  P(T('Date:')), blank(), blank(),
  P(T('[STUDENT 1 NAME]                                        [STUDENT 2 NAME]', { bold:true })),
  P(T('([REG NO. 1])                                                   ([REG NO. 2])')), blank(),
  P(T('Research supervisor                         HOD                                    Director', { bold:true })),
  P(T('[GUIDE NAME]                                  [HOD NAME]                       [DIRECTOR NAME]')),
  pageBreak());

// Acknowledgements
front.push(P(T('ACKNOWLEDGEMENTS', { bold:true, size:28 }), center), blank(),
  scaffold('personalise. Thank the guide by name for direction on scope and review of the analysis; the department for computing/lab access; any senior or reviewer who commented on drafts; families. Keep to one page, first person plural.'),
  pageBreak());

// Abstract (drafted)
front.push(P(T('ABSTRACT', { bold:true, size:28 }), center), blank(),
  P(T('Small satellites flown as rideshare passengers inherit their orbit from the primary customer, and the spring deployers that release them add at most one or two metres per second, which is too little to change that orbit in any useful way. This report examines an alternative: a magazine-fed electromagnetic deployer, named EMOCD, that ejects unmodified CubeSats from a host stage at a controlled, programmable velocity. An architecture trade between reluctance coilguns and linear synchronous motors led to an ironless double-sided linear motor working against a reusable permanent-magnet sled, selected for its efficiency and for imposing no modification on the satellite. The design stores twelve 3U CubeSats in two transverse cassettes feeding a single 1.5 m track, arrests the sled with a contactless eddy-current brake, and draws its pulse energy from a supercapacitor bank.')),
  P(T('Ten analyses were carried out to size and evaluate the system. The launch model predicts an exit velocity of 22.4 m/s at 19.7 g on the payload, within standard CubeSat qualification loads, at 52 percent net electrical efficiency and a closed-loop velocity dispersion of 0.054 m/s (3-sigma). Orbit-decay modelling shows a single 25 m/s prograde ejection roughly doubles a propulsion-less satellite\u2019s orbital lifetime, a result that holds across ballistic coefficient and deployment altitude. Differential ejection velocities of 2 to 10 m/s between satellites establish 30-degree constellation spacing in 1.4 to 6.9 days, against the weeks to months required by differential-drag phasing. Conjunction screening over 30 days, recoil budgets on a PSLV fourth-stage class host, tip-off and mass budgets complete the assessment. The system closes at roughly 105 kg dry within an ESPA Grande allocation. A staged validation path is proposed, ending in a captive-carry demonstration on ISRO\u2019s POEM platform.')),
  pageBreak());

// Contents (auto TOC field)
front.push(P(T('(Annexure 3)', { bold:true }), { alignment: AlignmentType.RIGHT }),
  P(T('CONTENTS', { bold:true, size:28 }), center),
  P(T('[Word: right-click the field below and choose Update Field (or press F9) to populate page numbers]', { italics:true, color:'808080', size:20 })),
  new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-2' }),
  pageBreak());

// List of figures/tables
front.push(P(T('(Annexure 4)', { bold:true }), { alignment: AlignmentType.RIGHT }),
  P(T('LIST OF FIGURES', { bold:true, size:28 }), center), blank(),
  simpleTable([
    ['Fig. 1','EMOCD system block diagram'],
    ['Fig. 2','Plan-view layout within the ESPA Grande envelope'],
    ['Fig. 3','[CAD] Full assembly model — isometric view (to be added)'],
    ['Fig. 4','[CAD] Sled and cassette detail views (to be added)'],
    ['Fig. 5','Shot profile: velocity, bank voltage and current'],
    ['Fig. 6','[FEMM] Halbach airgap flux-density map (to be added)'],
    ['Fig. 7','Monte Carlo exit-velocity dispersion, open vs closed loop'],
    ['Fig. 8','Eddy-brake arrest profile'],
    ['Fig. 9','Orbital lifetime vs deployment altitude, with and without boost'],
    ['Fig. 10','Along-track constellation spacing vs time for ejection-velocity splits'],
    ['Fig. 11','Satellite-stage separation distance over 30 days'],
    ['Fig. 12','Payload family: exit velocity and acceleration by class'],
    ['Fig. 13','Tip-off error budget against deployer requirements'],
    ['Fig. 14','System dry-mass breakdown'],
  ], [1200, 7800]), pageBreak());

// Abbreviations
front.push(P(T('(Annexure 5)', { bold:true }), { alignment: AlignmentType.RIGHT }),
  P(T('LIST OF ABBREVIATIONS', { bold:true, size:28 }), center), blank(),
  simpleTable([
    ['EMOCD','Electromagnetic Orbital CubeSat Deployer'],
    ['LSM','Linear Synchronous Motor'],
    ['CMG','Control Moment Gyroscope'],
    ['RCS','Reaction Control System'],
    ['ESPA','EELV Secondary Payload Adapter'],
    ['POEM','PSLV Orbital Experimental Module'],
    ['PS4','PSLV fourth stage'],
    ['PPU','Power Processing Unit'],
    ['SiC','Silicon Carbide'],
    ['BC','Ballistic Coefficient'],
    ['COLA','Collision Avoidance (analysis)'],
    ['NRCSD','NanoRacks CubeSat Deployer'],
    ['J-SSOD','JEM Small Satellite Orbital Deployer'],
    ['P-POD','Poly-Picosatellite Orbital Deployer'],
    ['GNC','Guidance, Navigation and Control'],
    ['NdFeB','Neodymium-Iron-Boron (magnet)'],
    ['MLI','Multi-Layer Insulation'],
    ['IMU','Inertial Measurement Unit'],
    ['ConOps','Concept of Operations'],
    ['EOL','End of Life'],
  ], [1500, 7500]), pageBreak());

// ---------- main body section (arabic numerals) ----------
const body = [];
const H1 = (t)=> new Paragraph({ heading: HeadingLevel.HEADING_1, children:[T(t,{bold:true,size:28})] });
const H2 = (t)=> new Paragraph({ heading: HeadingLevel.HEADING_2, children:[T(t,{bold:true,size:24})] });

// Chapter 1
body.push(H1('CHAPTER 1 — INTRODUCTION'),
  H2('1.1 Background'),
  scaffold('rideshare model and the secondary-payload orbit problem; spring deployers give 1-2 m/s with no orbital utility; the propulsion-less satellite class (university, cost-floor, policy-restricted) has no way to alter its orbit at all. 2-3 paragraphs.'),
  H2('1.2 Problem Statement'),
  scaffold('one tight paragraph: design a deployer that gives unmodified CubeSats a controlled, useful velocity increment within standard qualification loads, from a rideshare-compatible host, at acceptable mass.'),
  H2('1.3 Objectives'),
  scaffold('numbered objectives: architecture trade; system design (track, magazine, brake, power); ten quantitative analyses C1-C10; feasibility verdict; validation roadmap.'),
  H2('1.4 Scope and Limitations'),
  scaffold('PBL-2 scope is design and analysis: CAD, analytical models, FEMM verification. Benchtop hardware is future work. State the honest model limitations up front (static atmosphere, surface-current motor model, screening-level conjunction sampling).'),
  pageBreak());

// Chapter 2
body.push(H1('CHAPTER 2 — LITERATURE REVIEW'),
  H2('2.1 CubeSat Deployment Systems and Their Limits'),
  scaffold('P-POD, J-SSOD (1.1-1.7 m/s), NRCSD; the ESMATS 2018 ball-lock failure as the case study for preload-through-release-path design faults [refs 1-4].'),
  H2('2.2 Electromagnetic Launch'),
  scaffold('railgun vs coilgun physics; Sandia nanosatellite coilgun and induction launcher programs; efficiency record: 1-2% single-stage reluctance, up to ~45% large multistage induction [refs 5-6].'),
  H2('2.3 Linear Motors and Halbach Arrays'),
  scaffold('Halbach array field concentration; Inductrack ironless levitation as the closest architectural relative [refs 11-12, verify citations].'),
  H2('2.4 Pulsed Power for Small Spacecraft'),
  scaffold('supercapacitor qualification for space: ESA SPCD 2018 programme, SpaceCap results [refs 9-10].'),
  H2('2.5 Contactless Braking in Space Mechanisms'),
  scaffold('eddy-current damper flight heritage and why the properties suit vacuum [ref 15].'),
  H2('2.6 Constellation Phasing Without Propulsion'),
  scaffold('differential drag: Planet Labs Flock 2p campaign, weeks-to-months timescale [refs 7-8]. This is the benchmark EMOCD is measured against.'),
  H2('2.7 Host Platforms'),
  scaffold('POEM-1 through POEM-4: capabilities, 3U payload class, zero-debris precedent; OTV landscape in one paragraph for contrast [refs 13-14].'),
  H2('2.8 Research Gap'),
  scaffold('no published deployer operates between ~1.5 m/s springs and km/s ground guns. The 10-30 m/s regime is unclaimed. One paragraph, ends the chapter.'),
  pageBreak());

// Chapter 3
body.push(H1('CHAPTER 3 — METHODOLOGY'),
  H2('3.1 Requirements Definition'),
  scaffold('derive requirements: unmodified CubeSat, under 25-30 g, ESPA Grande envelope and mass, programmable velocity, 12-satellite manifest, abort and inhibit provisions, host-agnostic recoil handling.'),
  H2('3.2 Architecture Trade: Coilgun vs Linear Synchronous Motor'),
  scaffold('the payload g-limit sets a velocity ceiling (~31-42 m/s at 2-3 m stroke) that removes the coilgun\u2019s only advantage; efficiency 1-2% vs 50%+; the sled removes armature mass from the customer satellite; servo control and abort. Table 1 carries the trade.'),
  H2('3.3 System Architecture'),
  ...fig('D01_block.png','Fig. 1. EMOCD system block diagram.', 520),
  ...fig('D02_layout.png','Fig. 2. Plan-view layout within the ESPA Grande envelope (not to scale).', 520),
  scaffold('walk the firing cycle: feed, latch, accelerate, release at coast-trim, brake, return. Note the two free functions: inertia holds the satellite during acceleration; braking the sled is the release.'),
  placeholder('Fig. 3 — CAD assembly isometric (AVM)'),
  placeholder('Fig. 4 — CAD sled and cassette details (AVM)'),
  H2('3.4 Materials Selection'),
  scaffold('condense the materials table with the three governing rules: nothing conductive rides the field, nothing near the track is ferromagnetic except on purpose, nothing outgasses near customer optics. Table 2.'),
  H2('3.5 Analytical Models'),
  scaffold('present each model with its governing equations: Halbach surface field and gap decay; shot ODE with supercapacitor sag; King-Hele orbit-averaged decay; Kepler+J2 conjunction propagation; eddy-brake force law; tip-off angular-impulse budget. Cite the numerical methods.'),
  H2('3.6 Finite-Element Verification'),
  placeholder('Fig. 6 — FEMM magnetostatic airgap map (AVM, setup sheet provided)'),
  scaffold('describe the FEMM model: geometry, N45SH material curve, boundary conditions; compare peak and mean airgap field against the analytic 0.62 T.'),
  pageBreak());

// Chapter 4
body.push(H1('CHAPTER 4 — RESULTS AND DISCUSSION'),
  H2('4.1 Launch Performance'),
  ...fig('F01_shot_profile.png','Fig. 5. Shot profile: (a) velocity vs position with coast-trim zone; (b) bank voltage and current vs time.', 540),
  scaffold('22.4 m/s at 19.7 g; 125 ms pulse; 463 A peak; 4.6% sag; 2.47 kJ drawn, 1.92 kJ net after regen, 52% end-to-end.'),
  ...fig('F03_montecarlo.png','Fig. 7. Exit-velocity dispersion over 4000 Monte Carlo runs.', 440),
  H2('4.2 Sled Arrest'),
  ...fig('F08_brake.png','Fig. 8. Eddy-brake arrest profile with deceleration capped at 200 g by pole taper.', 440),
  H2('4.3 Astrodynamic Utility'),
  ...fig('F04_lifetime.png','Fig. 9. Orbital lifetime vs deployment altitude (BC = 61 kg/m\u00b2, mean solar activity model).', 440),
  ...fig('F05_drift.png','Fig. 10. Along-track separation vs time for ejection-velocity splits at 450 km.', 440),
  scaffold('the two headline results: 2.0x lifetime per 25 m/s shot, invariant across BC and altitude; 30-degree spacing in 1.4-6.9 days vs weeks-months for differential drag.'),
  H2('4.4 Deployment Safety'),
  ...fig('F06_conjunction.png','Fig. 11. Satellite-stage separation over 30 days, staggered firing, 25 m/s prograde.', 460),
  scaffold('62 km fleet minimum; 6.6-day phase realignment; 348 km if the stage disposes at day 2; screening-level caveat.'),
  H2('4.5 Host Interaction Budgets'),
  scaffold('per-shot 89.6 N s; PS4-class recoil and helium cost table; cumulative translation folded into disposal targeting.'),
  H2('4.6 Error and Tip-off Budgets'),
  ...fig('F09_tipoff.png','Fig. 13. Tip-off error budget against NRCSD-class requirements.', 440),
  scaffold('0.054 m/s maps to 0.19 km apogee placement; worst-case tip-off 3.9 deg/s.'),
  H2('4.7 Payload Family and System Budgets'),
  ...fig('F07_family.png','Fig. 12. Payload family: the system is force-limited, not g-limited, above 1U.', 420),
  ...fig('F10_mass.png','Fig. 14. Dry-mass breakdown (estimates pending CAD).', 460),
  H2('4.8 Discussion and Limitations'),
  scaffold('carry the six honest caveats from the results document verbatim in spirit: solar-activity dependence, surface-current model pending FEA, first-order brake law, sampling limits, PS4 mass as class range, pre-CAD masses.'),
  pageBreak());

// Chapter 5
body.push(H1('CHAPTER 5 — CONCLUSION AND FUTURE WORK'),
  H2('5.1 Conclusions'),
  scaffold('numbered conclusions mirroring the objectives: the LSM architecture closes; the performance figures; the two utility results; safety and host budgets; mass margin.'),
  H2('5.2 Future Work'),
  scaffold('the staged roadmap: FEMM-validated model (in progress), 0.5 m benchtop, full 1.5 m ground track with mass simulator, vacuum tribology tests, POEM captive-carry demonstration. Note EMOCD-F free-flyer variant in one paragraph.'),
  pageBreak());

// References
body.push(H1('REFERENCES'),
  ...[
    '[1] C. P. Lewis, "Failure of the Ball-Lock Mechanism on the NanoRacks CubeSat Deployer," Proc. 44th Aerospace Mechanisms Symposium / ESMATS, 2018.',
    '[2] JAXA, "JEM Payload Accommodation Handbook Vol. 8: Small Satellite Deployment Interface Control Document," via UNOOSA KiboCUBE.',
    '[3] NASA Small Spacecraft Systems Virtual Institute, "State-of-the-Art of Small Spacecraft Technology: Integration, Launch, Deployment, and Orbital Transport."',
    '[4] "Design and Analysis of a New Deployer for the in Orbit Release of Multiple Stacked CubeSats," Remote Sensing, vol. 14, no. 17, 4205, 2022.',
    '[5] B. N. Turman et al., "Coilgun Launcher for Nanosatellites," Sandia National Laboratories / OSTI conference report.',
    '[6] R. J. Kaye et al., "Electromagnetic Coilgun Launcher for Space Applications," Sandia National Laboratories, OSTI 125180.',
    '[7] C. Foster et al., "Constellation Phasing with Differential Drag on Planet Labs Satellites," Journal of Spacecraft and Rockets, vol. 55, no. 2, 2018 (arXiv:1806.01218).',
    '[8] C. Foster, H. Hallam, J. Mason, "Orbit Determination and Differential-Drag Control of Planet Labs CubeSat Constellations," arXiv:1509.03270, 2015.',
    '[9] F. Faure et al., "Qualification of COTS Supercapacitors for Space Applications," ESA Space Passive Component Days, 2018.',
    '[10] "Towards Supercapacitors in Space Applications," European Space Power Conference, 2017.',
    '[11] R. F. Post and D. D. Ryutov, "The Inductrack: A Simpler Approach to Magnetic Levitation," IEEE Trans. Applied Superconductivity, vol. 10, no. 1, 2000. [VERIFY full citation before submission]',
    '[12] K. Halbach, "Design of Permanent Multipole Magnets with Oriented Rare Earth Cobalt Material," Nuclear Instruments and Methods, vol. 169, 1980. [VERIFY full citation before submission]',
    '[13] ISRO, "PSLV-C58/XPoSat: POEM-3 Accomplishes Zero Orbital Debris Mission," March 2024.',
    '[14] "PSLV Orbital Experiment Module," Wikipedia (background; replace with ISRO primary sources where possible).',
    '[15] "Eddy Current Damper Modelling for Space Mechanisms," Actuators (MDPI) and CDA InterCorp flight-heritage documentation.',
    '[16] NanoRacks, "NanoRacks CubeSat Deployer (NRCSD) Interface Definition Document," 2018.',
    '[17] V. Yudintsev, "Separation Dynamics of CubeSats," (deployment tip-off analysis).',
    '[18] "Vibro-Impact Modelling of CubeSat Deployment," Aerospace Science and Technology, 2019. [VERIFY exact title/authors]',
    '[19] D. A. Vallado, Fundamentals of Astrodynamics and Applications, 4th ed., Microcosm Press (exponential atmosphere model, Table 8-4).',
    '[20] Airbus Defence and Space, "CMG 15-45 S" product datasheet, via satsearch.',
  ].map(t => P(T(t, { size: 22 }), { spacing: { line: 240, after: 120 } }))
);

// ---------- document ----------
const doc = new Document({
  styles: {
    default: { document: { run: { font: 'Times New Roman', size: 24 }, paragraph: { spacing: { line: 360, lineRule: LineRuleType.AUTO } } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: 'Times New Roman', size: 28, bold: true, color: '000000' },
        paragraph: { spacing: { before: 240, after: 240, line: 360, lineRule: LineRuleType.AUTO }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: 'Times New Roman', size: 24, bold: true, color: '000000' },
        paragraph: { spacing: { before: 200, after: 120, line: 360, lineRule: LineRuleType.AUTO }, outlineLevel: 1 } },
    ],
  },
  features: { updateFields: true },
  sections: [
    { properties: { page: { margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN },
        pageNumbers: { start: 1, formatType: NumberFormat.LOWER_ROMAN } } },
      footers: { default: new Footer({ children: [ new Paragraph({ alignment: AlignmentType.CENTER,
        children: [ new TextRun({ font:'Times New Roman', children: [PageNumber.CURRENT] }) ] }) ] }) },
      children: front },
    { properties: { type: SectionType.NEXT_PAGE, page: { margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN },
        pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL } } },
      footers: { default: new Footer({ children: [ new Paragraph({ alignment: AlignmentType.CENTER,
        children: [ new TextRun({ font:'Times New Roman', children: [PageNumber.CURRENT] }) ] }) ] }) },
      children: body },
  ],
});

Packer.toBuffer(doc).then(buf => { fs.writeFileSync('EMOCD_PBL2_Skeleton.docx', buf); console.log('written', buf.length, 'bytes'); });
