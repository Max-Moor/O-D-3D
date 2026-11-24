

(function () {

    const root = document.getElementById("quizRoot");

    const state = {
        step: 0,
        answers: {}
    };

    const questions = [

        {
            id: "purpose",
            title: "Quel est l'usage final de la pièce ?",
            subtitle: "Choisissez la description la plus proche de votre besoin.",
            options: [
                ["visual", "👁️", "Prototype visuel — je valide une forme ou un design, sans contrainte mécanique"],
                ["functional-test", "🧪", "Prototype fonctionnel — je teste la pièce en conditions réelles avant la série"],
                ["final-unique", "🏆", "Pièce définitive — un seul exemplaire final"],
                ["final-series", "📦", "Pièce définitive — plusieurs exemplaires identiques"],
                ["replacement", "🔧", "Pièce de remplacement — remplacer une pièce cassée ou introuvable"]
            ]
        },

        {
            id: "quantity",
            title: "Combien d'exemplaires souhaitez-vous ?",
            subtitle: "Une estimation suffit.",
            options: [
                ["one", "1", "1 seule pièce"],
                ["small", "2–10", "2 à 10 pièces"],
                ["medium", "10–50", "10 à 50 pièces"],
                ["large", "50+", "Plus de 50 pièces"]
            ]
        },

        {
            id: "cadFile",
            title: "Disposez-vous déjà d'un fichier 3D de la pièce ?",
            subtitle: "Cela détermine si nous devons d'abord modéliser ou scanner votre pièce.",
            options: [
                ["file-ready", "📁", "Oui, un fichier 3D prêt (STL, STEP, etc.)"],
                ["plans", "📐", "J'ai des plans ou des croquis, mais pas de fichier 3D"],
                ["physical-object", "📷", "Non, je pars d'un objet physique existant à reproduire"],
                ["idea-only", "💡", "Non, juste une idée à définir ensemble"]
            ]
        },

        {
            id: "size",
            title: "Quelle est la plus grande dimension de la pièce ?",
            subtitle: "Longueur, largeur ou hauteur — prenez la plus grande des trois.",
            options: [
                ["small", "◽", "Moins de 10 cm"],
                ["medium", "◻️", "10 à 30 cm"],
                ["large", "⬛", "30 cm à 1 m"],
                ["veryLarge", "🗿", "Plus d'1 m"],
                ["unknown", "❓", "Je ne sais pas encore"]
            ]
        },

        {
            id: "wallThickness",
            title: "Quelle est l'épaisseur de l'endroit le plus fin de la pièce ?",
            subtitle: "Par exemple une languette, une paroi ou un détail fin. Une estimation suffit.",
            options: [
                ["thick", "▮", "Plus de 3 mm"],
                ["medium", "▯", "1 à 3 mm"],
                ["thin", "│", "0,5 à 1 mm"],
                ["veryThin", "┆", "Moins de 0,5 mm"],
                ["unknown", "❓", "Je ne sais pas"]
            ]
        },

        {
            id: "internalFeatures",
            title: "La pièce contient-elle des cavités ou canaux internes fermés ?",
            subtitle: "Par exemple un canal de refroidissement, une forme creuse fermée, ou une géométrie impossible à atteindre avec un outil de fraisage.",
            options: [
                ["none", "○", "Non, forme pleine ou ouverte"],
                ["some", "◐", "Quelques détails internes accessibles"],
                ["closed", "🌀", "Oui, cavité ou canal totalement fermé"],
                ["unknown", "❓", "Je ne sais pas"]
            ]
        },

        {
            id: "tolerance",
            title: "Quelle tolérance dimensionnelle est nécessaire ?",
            subtitle: "Pensez à un ajustement avec une autre pièce, un axe, un filetage ou un roulement.",
            options: [
                ["none", "±0,5 mm", "Pas de contrainte particulière"],
                ["medium", "±0,2–0,3 mm", "Ajustement standard entre deux pièces"],
                ["tight", "±0,1 mm ou moins", "Ajustement précis (axe, roulement, filetage fin)"],
                ["unknown", "❓", "Je ne sais pas"]
            ]
        },

        {
            id: "surfaceFinish",
            title: "Quel état de surface recherchez-vous ?",
            subtitle: "Aspect visuel et au toucher, une fois la pièce terminée.",
            options: [
                ["functional", "🔩", "Fonctionnel — les traces de fabrication ne posent pas de problème"],
                ["clean", "🧼", "Propre — légèrement poncée ou peinte si besoin"],
                ["smooth", "✨", "Lisse dès la sortie machine"],
                ["mirror", "💎", "Quasi miroir / polie (type bijouterie, vitrine)"]
            ]
        },

        {
            id: "mechanicalLoad",
            title: "Quelle charge mécanique la pièce devra-t-elle supporter ?",
            subtitle: "Pensez au poids porté, aux chocs, et à la fréquence d'utilisation.",
            options: [
                ["none", "🎨", "Aucune — pièce purement esthétique ou décorative"],
                ["light", "✋", "Manipulation occasionnelle, faible poids"],
                ["moderate", "⚙️", "Utilisation régulière, charge modérée"],
                ["heavy", "🏋️", "Charge importante, chocs ou usage intensif répété"]
            ]
        },

        {
            id: "flexRequired",
            title: "La pièce doit-elle être souple ou élastique ?",
            subtitle: "Par exemple un joint, une poignée souple, ou un amortisseur.",
            options: [
                ["rigid", "🧱", "Non, elle doit rester rigide"],
                ["some", "〰️", "Un peu de souplesse est acceptable"],
                ["flexible", "🎈", "Oui, elle doit être souple"],
                ["veryFlexible", "🩸", "Très souple / élastique"]
            ]
        },

        {
            id: "temperature",
            title: "À quelle température maximale la pièce sera-t-elle exposée en usage normal ?",
            subtitle: "Une estimation suffit — pensez au pire cas d'usage.",
            options: [
                ["ambient", "🌡️", "Température ambiante, moins de 45°C"],
                ["medium", "🌤️", "45 à 80°C"],
                ["high", "🔥", "80 à 150°C"],
                ["veryHigh", "🌋", "Plus de 150°C"],
                ["unknown", "❓", "Je ne sais pas"]
            ]
        },

        {
            id: "environment",
            title: "Quelle est la contrainte d'environnement la plus déterminante ?",
            subtitle: "Choisissez celle qui compte le plus pour le choix du matériau.",
            options: [
                ["indoor", "🏠", "Intérieur, environnement contrôlé"],
                ["outdoor", "☀️", "Extérieur, exposée aux UV et aux intempéries"],
                ["moisture", "💧", "Humidité fréquente ou immersion dans l'eau"],
                ["chemical", "🧪", "Contact avec solvants, huiles ou produits chimiques"],
                ["food", "🍽️", "Contact alimentaire direct"],
                ["esd", "⚡", "Proximité de composants électroniques sensibles (ESD)"],
                ["fire", "🚨", "Norme feu / ignifugation requise"],
                ["medical", "🩺", "Usage médical ou dentaire"],
                ["jewelry", "💍", "Fonderie / bijouterie (coulée à la cire perdue)"]
            ]
        },

        {
            id: "materialConstraint",
            title: "La pièce doit-elle être usinée dans un bloc de matière massif ?",
            subtitle: "Par exemple pour obtenir un métal plein, plutôt qu'une pièce construite couche par couche.",
            options: [
                ["metal", "🔩", "Oui, nécessite un métal usiné (aluminium, laiton...)"],
                ["solid-plastic", "⬛", "Oui, un plastique usiné dans la masse"],
                ["no", "🖨️", "Non, l'impression 3D convient parfaitement"],
                ["unknown", "❓", "Je ne sais pas"]
            ]
        }
    ];

    function progress() {

        if (state.step >= questions.length) {
            return 100;
        }

        return Math.round((state.step / questions.length) * 100);
    }

    function render() {

        root.innerHTML = `
            <div class="qz-top">
                <div class="qz-eyebrow">O&D 3D · Guide de fabrication</div>
                <div class="qz-progress">
                    <div class="qz-progressBar" style="width:${progress()}%"></div>
                </div>
            </div>

            <div class="qz-content">
                ${getContent()}
            </div>

            ${getFooter()}
        `;

        bindEvents();
    }

    function getContent() {

        if (state.step < questions.length) {

            const q = questions[state.step];

            return `
                <h2 class="qz-h1">${q.title}</h2>
                <div class="qz-subtitle">${q.subtitle}</div>
                <div class="qz-options">
                    ${q.options.map(option => `
                        <button type="button" class="qz-option" data-value="${option[0]}">
                            <span class="qz-icon">${option[1]}</span>
                            ${option[2]}
                        </button>
                    `).join("")}
                </div>
            `;
        }

        return getResult();
    }

    function getFooter() {

        if (state.step >= questions.length) {
            return "";
        }

        return `
            <div class="qz-footer">
                ${
                    state.step > 0
                        ? `<button type="button" class="qz-back" id="back">← Question précédente</button>`
                        : `<span></span>`
                }
                <span class="qz-counter">${state.step + 1} / ${questions.length}</span>
            </div>
        `;
    }

    function getResult() {

        const result = calculateResult();

        return `
            <div class="qz-resultHeader">
                <div class="qz-resultIcon">${result.icon}</div>
                <div class="qz-confidence">TECHNOLOGIE RECOMMANDÉE</div>
                <div class="qz-tech">${result.tech}</div>
                <div class="qz-material">${result.material}</div>
                <div class="qz-confidence">Niveau de pertinence : ${result.score}%</div>
            </div>

            <div class="qz-card">
                <div class="qz-cardTitle">Pourquoi cette solution ?</div>
                <div class="qz-why">${result.reason}</div>
            </div>

            <div class="qz-card">
                <div class="qz-cardTitle">✓ Les avantages</div>
                <div class="qz-pros">
                    ${result.pros.map(x => `<div class="qz-pro">✓ ${x}</div>`).join("")}
                </div>
            </div>

            <div class="qz-card">
                <div class="qz-cardTitle">⚠ Points d'attention</div>
                <div class="qz-cons">
                    ${result.cons.map(x => `<div class="qz-con">⚠ ${x}</div>`).join("")}
                </div>
            </div>

            <div class="qz-card">
                <div class="qz-cardTitle">Votre demande</div>
                <div class="qz-why">${summary()}</div>
            </div>

            <div class="qz-card">
                <div class="qz-contact">
                    Cette recommandation constitue une première orientation.
                    O&D 3D valide le choix définitif en fonction de votre fichier 3D
                    et des contraintes réelles de votre projet.
                    <br><br>
                    <a href="../contact/" style="color:#00d4ff;">
                        Contactez-nous pour valider votre projet →
                    </a>
                </div>
            </div>

            <button type="button" class="qz-restart" id="restart">
                ↺ Recommencer le quiz
            </button>
        `;
    }

    function summary() {

        const labels = {
            purpose: "Usage final",
            quantity: "Quantité",
            cadFile: "Fichier 3D",
            size: "Dimension max.",
            wallThickness: "Épaisseur mini.",
            internalFeatures: "Cavités internes",
            tolerance: "Tolérance",
            surfaceFinish: "État de surface",
            mechanicalLoad: "Charge mécanique",
            flexRequired: "Souplesse",
            temperature: "Température max.",
            environment: "Environnement",
            materialConstraint: "Matériau massif"
        };

        return Object.entries(state.answers)
            .map(([key, value]) => {

                const q = questions.find(question => question.id === key);
                const option = q ? q.options.find(item => item[0] === value) : null;

                return `<strong>${labels[key] || key}</strong> : ${option ? option[2] : value}<br>`;
            })
            .join("");
    }

    function calculateResult() {

        const scores = { FDM: 0, SLS: 0, RESINE: 0, CNC: 0 };
        const a = state.answers;

        if (a.purpose === "visual") { scores.RESINE += 8; scores.FDM += 10; }
        if (a.purpose === "functional-test") { scores.FDM += 10; scores.SLS += 10; scores.CNC += 6; }
        if (a.purpose === "final-series") { scores.SLS += 14; scores.FDM += 6; }
        if (a.purpose === "final-unique") { scores.FDM += 6; scores.SLS += 6; scores.CNC += 8; scores.RESINE += 6; }
        if (a.purpose === "replacement") { scores.FDM += 8; scores.SLS += 6; scores.CNC += 6; }

        if (a.quantity === "one") { scores.FDM += 4; scores.RESINE += 4; scores.CNC += 3; }
        if (a.quantity === "small") { scores.SLS += 8; scores.FDM += 5; }
        if (a.quantity === "medium") { scores.SLS += 14; scores.FDM += 6; }
        if (a.quantity === "large") { scores.SLS += 18; scores.FDM += 8; scores.RESINE -= 4; }

        if (a.wallThickness === "medium") { scores.FDM += 3; scores.SLS += 3; }
        if (a.wallThickness === "thin") { scores.SLS += 8; scores.RESINE += 6; scores.FDM -= 4; scores.CNC -= 6; }
        if (a.wallThickness === "veryThin") { scores.RESINE += 12; scores.SLS += 6; scores.FDM -= 8; scores.CNC -= 10; }

        if (a.internalFeatures === "some") { scores.SLS += 6; }
        if (a.internalFeatures === "closed") { scores.SLS += 16; scores.CNC -= 15; scores.FDM -= 6; }

        if (a.tolerance === "medium") { scores.CNC += 4; scores.SLS += 3; }
        if (a.tolerance === "tight") { scores.CNC += 14; scores.RESINE += 8; scores.SLS += 4; scores.FDM -= 6; }

        if (a.surfaceFinish === "functional") { scores.FDM += 4; }
        if (a.surfaceFinish === "clean") { scores.FDM += 2; scores.SLS += 3; }
        if (a.surfaceFinish === "smooth") { scores.RESINE += 10; scores.CNC += 8; }
        if (a.surfaceFinish === "mirror") { scores.RESINE += 18; scores.CNC += 12; scores.FDM -= 6; }

        if (a.mechanicalLoad === "none") { scores.RESINE += 8; }
        if (a.mechanicalLoad === "light") { scores.FDM += 4; scores.RESINE += 4; }
        if (a.mechanicalLoad === "moderate") { scores.FDM += 8; scores.SLS += 8; scores.CNC += 6; scores.RESINE -= 8; }
        if (a.mechanicalLoad === "heavy") { scores.CNC += 14; scores.SLS += 12; scores.FDM += 8; scores.RESINE -= 20; }

        if (a.flexRequired === "some") { scores.FDM += 3; scores.SLS += 3; }
        if (a.flexRequired === "flexible") { scores.FDM += 8; scores.SLS += 8; }
        if (a.flexRequired === "veryFlexible") { scores.SLS += 10; scores.FDM += 6; }

        if (a.temperature === "medium") { scores.FDM += 5; }
        if (a.temperature === "high") { scores.FDM += 10; scores.CNC += 6; }
        if (a.temperature === "veryHigh") { scores.FDM += 16; scores.CNC += 8; scores.SLS += 4; }

        if (a.environment === "outdoor") { scores.FDM += 8; scores.SLS += 4; scores.RESINE -= 6; }
        if (a.environment === "moisture") { scores.FDM += 6; scores.SLS += 6; scores.CNC += 4; scores.RESINE -= 6; }
        if (a.environment === "chemical") { scores.FDM += 6; scores.SLS += 6; scores.CNC += 6; }
        if (a.environment === "food") { scores.SLS += 14; scores.FDM += 6; }
        if (a.environment === "esd") { scores.SLS += 22; }
        if (a.environment === "fire") { scores.SLS += 10; scores.FDM += 8; }
        if (a.environment === "medical") { scores.RESINE += 20; }
        if (a.environment === "jewelry") { scores.RESINE += 35; }

        if (a.materialConstraint === "metal") { scores.CNC += 40; scores.FDM -= 10; scores.SLS -= 10; scores.RESINE -= 15; }
        if (a.materialConstraint === "solid-plastic") { scores.CNC += 28; scores.FDM -= 6; scores.SLS -= 6; }

        const sorted = Object.entries(scores).sort((x, y) => y[1] - x[1]);
        const winner = sorted[0][0];
        const max = Math.max(...Object.values(scores));
        const min = Math.min(...Object.values(scores));

        let confidence = 70;

        if (max > min) {
            confidence = Math.min(98, Math.max(65, Math.round(70 + ((max - sorted[1][1]) * 1.5))));
        }

        return buildRecommendation(winner, confidence);
    }

    function buildRecommendation(tech, score) {

        const a = state.answers;

        if (tech === "CNC") {

            let material = "POM / Nylon (usinage CNC)";

            if (a.materialConstraint === "metal") {
                material = a.mechanicalLoad === "heavy" ? "Aluminium (usinage CNC)" : "Aluminium ou Laiton (usinage CNC)";
            } else if (a.surfaceFinish === "mirror") {
                material = "Laiton ou Aluminium poli (usinage CNC)";
            } else if (a.tolerance === "tight") {
                material = "POM (Delrin) — usinage CNC";
            }

            return {
                tech: "CNC",
                material,
                icon: "⚙️",
                score,
                reason: "Vos réponses indiquent qu'un usinage dans un matériau massif est particulièrement pertinent : tolérance serrée, finition premium ou nécessité d'un métal plein. Le CNC est recommandé lorsque la précision dimensionnelle et les propriétés du matériau massif priment.",
                pros: [
                    "Très bonne précision dimensionnelle",
                    "Excellente qualité de finition",
                    "Propriétés du matériau massif conservées",
                    "Aluminium, Laiton, POM, Nylon et bois disponibles"
                ],
                cons: [
                    "Certaines géométries internes fermées sont inaccessibles à l'outil",
                    "Plus de matière est retirée pendant l'usinage",
                    "Moins avantageux pour de très petites séries de pièces complexes"
                ]
            };
        }

        if (tech === "RESINE") {

            let material = "Résine Standard";
            let reason = "Vos réponses donnent la priorité à la précision, aux détails fins ou à la qualité de surface. La résine SLA/MSLA est particulièrement adaptée aux prototypes visuels, aux pièces très détaillées et aux finitions premium.";

            if (a.environment === "jewelry") {
                material = "Résine Castable";
                reason = "Votre projet est destiné à la fonderie ou à la bijouterie. La Résine Castable est spécifiquement conçue pour les masters de coulée à la cire perdue.";
            }

            if (a.environment === "medical") {
                material = "Résine Biocompatible";
                reason = "Votre application est médicale ou dentaire. Une résine biocompatible adaptée à l'application est nécessaire.";
            }

            return {
                tech: "Résine SLA / MSLA",
                material,
                icon: "💎",
                score,
                reason,
                pros: [
                    "Très grande précision dimensionnelle",
                    "Excellente qualité de surface",
                    "Détails fins reproduits fidèlement",
                    "Très adaptée aux parois fines et aux finitions premium"
                ],
                cons: [
                    "Résistance mécanique généralement plus limitée qu'un plastique technique imprimé ou usiné",
                    "Résistance thermique limitée pour la résine standard",
                    "Post-traitement nécessaire"
                ]
            };
        }

        if (tech === "SLS") {

            let material = "PA12";
            let reason = "Vos réponses indiquent un besoin de pièces fonctionnelles, de petites séries ou d'une géométrie complexe. Le SLS est particulièrement intéressant lorsque la liberté de forme et l'absence de supports sont déterminantes.";

            if (a.environment === "esd") {
                material = "PA11-ESD";
                reason = "Votre pièce est destinée à la manipulation de composants électroniques sensibles. Un matériau ESD adapté est particulièrement pertinent pour cette application.";
            }

            if (a.environment === "food") {
                material = "PA12 Alimentaire";
                reason = "Votre pièce doit être en contact avec des aliments. Un PA12 adapté au contact alimentaire est à privilégier, sous réserve des exigences réglementaires précises de l'application.";
            }

            if (a.environment === "fire") {
                material = "PA2210 FR";
                reason = "Votre projet nécessite une propriété ignifuge. Un matériau FR adapté est à sélectionner selon la norme précise de votre application.";
            }

            if (a.flexRequired === "flexible" || a.flexRequired === "veryFlexible") {
                material = "TPU (SLS)";
                reason = "Votre pièce doit être souple ou élastique. Le TPU en SLS permet d'obtenir des pièces flexibles avec une géométrie complexe et sans support.";
            }

            if (a.mechanicalLoad === "heavy" && a.materialConstraint !== "metal") {
                material = "PA12-GF";
                reason = "Votre pièce doit supporter une charge mécanique importante. Un PA12 renforcé peut offrir une meilleure rigidité et stabilité dimensionnelle.";
            }

            return {
                tech: "SLS",
                material,
                icon: "🌡️",
                score,
                reason,
                pros: [
                    "Géométries complexes et cavités internes fabriquées sans supports",
                    "Très adapté aux pièces fonctionnelles",
                    "Excellent pour les petites et moyennes séries",
                    "Bonne tenue mécanique globale"
                ],
                cons: [
                    "Surface légèrement granuleuse en sortie machine",
                    "Coût généralement supérieur au FDM pour une pièce unique",
                    "Délai généralement plus long que le FDM"
                ]
            };
        }

        let material = "PETG";
        let reason = "Vos réponses correspondent bien à une fabrication FDM : solution polyvalente, intéressante pour le prototypage et les pièces fonctionnelles, avec un bon rapport coût / délai.";

        if (a.purpose === "visual" && a.mechanicalLoad === "none") {
            material = "PLA";
            reason = "Votre pièce est un prototype visuel sans contrainte mécanique. Le PLA est adapté au prototypage rapide et aux maquettes.";
        }

        if (a.environment === "outdoor") {
            material = "ASA";
            reason = "Votre pièce sera utilisée à l'extérieur. L'ASA est particulièrement adapté aux applications exposées aux UV et aux intempéries.";
        }

        if (a.environment === "chemical") {
            material = "PP";
            reason = "Votre pièce doit résister à des produits chimiques. Le PP présente une bonne résistance chimique parmi les matériaux FDM.";
        }

        if (a.flexRequired === "flexible" || a.flexRequired === "veryFlexible") {
            material = "TPU";
            reason = "Votre pièce doit être souple ou élastique. Le TPU est adapté aux pièces flexibles, joints et amortisseurs.";
        }

        if (a.temperature === "veryHigh") {
            material = "PEEK / PEKK / ULTEM";
            reason = "Votre pièce sera exposée à des températures très élevées. Des matériaux techniques haute température comme PEEK, PEKK ou certaines qualités d'ULTEM peuvent être envisagés selon les contraintes précises.";
        } else if (a.temperature === "high" && a.mechanicalLoad === "heavy") {
            material = "PA12-CF";
            reason = "Votre pièce combine une température de service élevée et une charge mécanique importante. Un PA renforcé en fibre de carbone peut apporter davantage de rigidité et de stabilité.";
        }

        return {
            tech: "FDM / FFF",
            material,
            icon: "🖨️",
            score,
            reason,
            pros: [
                "Solution polyvalente et généralement économique",
                "Adapté aux prototypes comme aux pièces fonctionnelles",
                "Large choix de matériaux techniques",
                "Possibilité de fabriquer de grandes dimensions"
            ],
            cons: [
                "Aspect des couches visible selon la finition demandée",
                "Résistance mécanique dépendante de l'orientation d'impression",
                "Les parois très fines sont difficiles à reproduire fidèlement"
            ]
        };
    }

    function bindEvents() {

        root.querySelectorAll(".qz-option").forEach(button => {

            button.addEventListener("click", () => {

                const q = questions[state.step];

                if (!q) {
                    return;
                }

                state.answers[q.id] = button.dataset.value;
                state.step++;
                render();
                { const _r = document.getElementById("quizApp"); window.scrollTo({ top: _r.getBoundingClientRect().top + scrollY - 90, behavior: "smooth" }); }
            });
        });

        const back = root.querySelector("#back");

        if (back) {
            back.addEventListener("click", () => {
                if (state.step > 0) {
                    state.step--;
                    render();
                }
            });
        }

        const restart = root.querySelector("#restart");

        if (restart) {
            restart.addEventListener("click", () => {
                state.step = 0;
                state.answers = {};
                render();
                { const _r = document.getElementById("quizApp"); window.scrollTo({ top: _r.getBoundingClientRect().top + scrollY - 90, behavior: "smooth" }); }
            });
        }
    }

    render();

})();

