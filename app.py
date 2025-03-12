from flask import Flask, request, redirect, url_for, jsonify, render_template_string, render_template
import numpy as np
import webview
import threading

app = Flask(__name__)

# Constantes pour le calcul de D_AB
D_AB_0_A = 2.1e-5
D_AB_0_B = 2.67e-5
phi_A = 0.279
phi_B = 0.721
lambda_A = 1.127
lambda_B = 0.973
q_A = 1.432
q_B = 1.4
theta_BA = 0.612
theta_BB = 0.739
theta_AB = 0.261
theta_AA = 0.388
tau_BA = 0.5373
tau_AB = 1.035
D_AB_reference = 1.33e-5  # Valeur de référence pour D_AB

# Page d'accueil
@app.route('/')
def home():
    return render_template_string("""
        <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f4f4f9;
                    }

                    h1 {
                        text-align: center;
                        color: #333;
                    }

                    p {
                        font-size: 16px;
                        color: #666;
                    }

                    button {
                        background-color: #4CAF50;
                        color: white;
                        padding: 10px 20px;
                        border: none;
                        cursor: pointer;
                        font-size: 16px;
                    }

                    button:hover {
                        background-color: #45a049;
                    }

                    a {
                        display: block;
                        text-align: center;
                        margin-top: 20px;
                        text-decoration: none;
                        color: #007BFF;
                    }

                    a:hover {
                        text-decoration: underline;
                    }
                </style>
            </head>
            <body>
                <h1>Bonjour👋</h1>
                <center><p>Bienvenue dans le calculateur du coefficient de diffusion.</p></center>
                <a href='/coeff-diffusion'><button>Suivant</button></a>
            </body>
        </html>
    """)

# Route pour le calculateur de coefficient de diffusion
@app.route('/coeff-diffusion', methods=['GET', 'POST'])
def coeff_diffusion():
    if request.method == 'POST':
        try:
            # Récupérer les valeurs de xA et xB
            xA = float(request.form['xA'])
            xB = float(request.form['xB'])

            # Vérifier que xA + xB = 1
            if abs(xA + xB - 1) > 1e-6:
                return render_template_string("""
                    <html>
                        <head>
                            <style>
                                body {
                                    font-family: Arial, sans-serif;
                                    margin: 0;
                                    padding: 0;
                                    background-color: #f4f4f9;
                                }

                                h1 {
                                    text-align: center;
                                    color: #333;
                                }

                                p {
                                    font-size: 16px;
                                    color: #666;
                                }

                                a {
                                    display: block;
                                    text-align: center;
                                    margin-top: 20px;
                                    text-decoration: none;
                                    color: #007BFF;
                                }

                                a:hover {
                                    text-decoration: underline;
                                }
                            </style>
                        </head>
                        <body>
                            <h1>Erreur</h1>
                            <p>La somme de x<sub>A</sub> et x<sub>B</sub> doit être égale à 1.</p>
                            <a href="/coeff-diffusion">Retour</a>
                        </body>
                    </html>
                """)

            # Calcul des termes de la formule
            term1 = xB * np.log(D_AB_0_A) + xA * np.log(D_AB_0_B)
            term2 = 2 * (xA * np.log(xA / phi_A) + xB * np.log(xB / phi_B))
            term3 = 2 * xA * xB * ((phi_A / xA) * (1 - (lambda_A / lambda_B)) + (phi_B / xB) * (1 - (lambda_B / lambda_A)))
            term4 = (xB * q_A) * ((1 - theta_BA ** 2) * np.log(tau_BA) + (1 - theta_BB ** 2) * tau_AB * np.log(tau_AB))
            term5 = (xA * q_B) * ((1 - theta_AB ** 2) * np.log(tau_AB) + (1 - theta_AA ** 2) * tau_BA * np.log(tau_BA))

            # Calcul de D_AB
            ln_D_AB = term1 + term2 + term3 + term4 + term5
            D_AB_calcule = np.exp(ln_D_AB)

            # Calcul de l'erreur
            erreur = abs((D_AB_calcule - D_AB_reference) / D_AB_reference) * 100

            # Affichage des résultats
            return render_template_string("""
                <html>
                    <head>
                        <style>
                            body {
                                font-family: Arial, sans-serif;
                                margin: 0;
                                padding: 0;
                                background-color: #f4f4f9;
                            }

                            h1 {
                                text-align: center;
                                color: #333;
                            }

                            p {
                                font-size: 16px;
                                color: #666;
                            }

                            a {
                                display: block;
                                text-align: center;
                                margin-top: 20px;
                                text-decoration: none;
                                color: #007BFF;
                            }

                            a:hover {
                                text-decoration: underline;
                            }
                        </style>
                    </head>
                    <body>
                        <h1>Résultat du calcul</h1>
                        <p>Le coefficient de diffusion D<sub>AB</sub> est : {{ D_AB_calcule:.4e }} cm²/s</p>
                        <p>L'erreur relative par rapport à la valeur expérimentale est : {{ erreur:.1f }}%</p>
                        <a href="/">Retour à l'accueil</a>
                    </body>
                </html>
            """, D_AB_calcule=D_AB_calcule, erreur=erreur)

        except ValueError:
            return render_template_string("""
                <html>
                    <head>
                        <style>
                            body {
                                font-family: Arial, sans-serif;
                                margin: 0;
                                padding: 0;
                                background-color: #f4f4f9;
                            }

                            h1 {
                                text-align: center;
                                color: #333;
                            }

                            p {
                                font-size: 16px;
                                color: #666;
                            }

                            a {
                                display: block;
                                text-align: center;
                                margin-top: 20px;
                                text-decoration: none;
                                color: #007BFF;
                            }

                            a:hover {
                                text-decoration: underline;
                            }
                        </style>
                    </head>
                    <body>
                        <h1>Erreur</h1>
                        <p>Veuillez saisir des valeurs numériques valides pour x<sub>A</sub> et x<sub>B</sub>.</p>
                        <a href="/coeff-diffusion">Retour</a>
                    </body>
                </html>
            """)

        except Exception as e:
            return render_template_string("""
                <html>
                    <head>
                        <style>
                            body {
                                font-family: Arial, sans-serif;
                                margin: 0;
                                padding: 0;
                                background-color: #f4f4f9;
                            }

                            h1 {
                                text-align: center;
                                color: #333;
                            }

                            p {
                                font-size: 16px;
                                color: #666;
                            }

                            a {
                                display: block;
                                text-align: center;
                                margin-top: 20px;
                                text-decoration: none;
                                color: #007BFF;
                            }

                            a:hover {
                                text-decoration: underline;
                            }
                        </style>
                    </head>
                    <body>
                        <h1>Erreur</h1>
                        <p>Une erreur inattendue s'est produite : {{ error }}</p>
                        <a href="/coeff-diffusion">Retour</a>
                    </body>
                </html>
            """, error=str(e))

    # Affichage du formulaire (méthode GET)
    return render_template_string("""
        <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f4f4f9;
                    }

                    h1 {
                        text-align: center;
                        color: #333;
                    }

                    form {
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                        background-color: white;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }

                    input[type="text"] {
                        width: 100%;
                        padding: 8px;
                        margin: 5px 0 15px 0;
                        border: 1px solid #ccc;
                        border-radius: 4px;
                    }

                    button {
                        background-color: #4CAF50;
                        color: white;
                        padding: 10px 20px;
                        border: none;
                        cursor: pointer;
                        font-size: 16px;
                    }

                    button:hover {
                        background-color: #45a049;
                    }

                    a {
                        display: block;
                        text-align: center;
                        margin-top: 20px;
                        text-decoration: none;
                        color: #007BFF;
                    }

                    a:hover {
                        text-decoration: underline;
                    }
                </style>
            </head>
            <body>
                <h1>Calculateur de coefficient de diffusion D<sub>AB</sub></h1>
                <form method="post">
                    Fraction molaire de A (x<sub>A</sub>) : <input type="text" name="xA" value="0.5" required><br><br>
                    Fraction molaire de B (x<sub>B</sub>) : <input type="text" name="xB" value="0.5" required><br><br>
                    <button type="submit">Calculer</button>
                </form>
            </body>
        </html>
    """)

# Gestion de l'erreur 404 (page non trouvée)
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Cette page n'existe pas !"}), 404

# Gestion de l'erreur 500 (erreur serveur)
@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Erreur interne du serveur"}), 500

# Fonction pour lancer Flask dans un thread séparé
def start_flask():
    app.run(debug=False, port=5000)

# Fonction pour lancer pywebview
def start_webview():
    webview.create_window("Calculateur de Coefficient de Diffusion", "http://127.0.0.1:5000/", width=800, height=600)
    webview.start()

if __name__ == '__main__':
    # Démarrer Flask dans un thread séparé
    threading.Thread(target=start_flask).start()

    # Démarrer pywebview
    start_webview()