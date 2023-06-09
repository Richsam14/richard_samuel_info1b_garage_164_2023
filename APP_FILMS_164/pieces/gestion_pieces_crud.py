"""Gestion des "routes" FLASK et des données pour les genres.
Fichier : gestion_genres_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.genres.gestion_genres_wtf_forms import FormWTFAjouterGenres
from APP_FILMS_164.genres.gestion_genres_wtf_forms import FormWTFDeleteGenre
from APP_FILMS_164.genres.gestion_genres_wtf_forms import FormWTFUpdateGenre
from APP_FILMS_164.pieces.gestion_pieces_wtf_forms import FormWTFAjouterPieces, FormWTFUpdatePiece, FormWTFDeletePiece

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /genres_afficher
    
    Test : ex : http://127.0.0.1:5575/genres_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les genres.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/pieces_afficher/<string:order_by>/<int:id_piece_sel>", methods=['GET', 'POST'])
def pieces_afficher(order_by, id_piece_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_piece_sel == 0:
                    strsql_pieces_afficher = """select * from t_piece"""
                    mc_afficher.execute(strsql_pieces_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR Passer une
                    #  commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_piece_selected_dictionnaire = {"value_id_piece_selected": id_piece_sel}
                    strsql_pieces_afficher = """select * from t_piece where id_piece = %(value_id_piece_selected)s"""

                    mc_afficher.execute(strsql_pieces_afficher, valeur_id_piece_selected_dictionnaire)
                else:
                    strsql_pieces_afficher = """select * from t_piece"""

                    mc_afficher.execute(strsql_pieces_afficher)

                data_pieces = mc_afficher.fetchall()

                print("data_pieces ", data_pieces, " Type : ", type(data_pieces))

                # Différencier les messages si la table est vide.
                if not data_pieces and id_piece_sel == 0:
                    flash("""La table "t_piece" est vide. !!""", "warning")
                elif not data_pieces and id_piece_sel > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"La piece demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données pieces affichés !!", "success")

        except Exception as Exception_pieces_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{pieces_afficher.__name__} ; "
                                          f"{Exception_pieces_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("pieces/pieces_afficher.html", data=data_pieces)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /pieces_ajouter
    
    Test : ex : http://127.0.0.1:5575/pieces_ajouter
    
    Paramètres : sans
    
    But : Ajouter un genre pour un film
    
    Remarque :  Dans le champ "name_genre_html" du formulaire "pieces/pieces_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/pieces_ajouter", methods=['GET', 'POST'])
def pieces_ajouter_wtf():
    form = FormWTFAjouterPieces()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                num_serie_piece_wtf = form.num_serie_piece_wtf.data
                num_serie_piece = num_serie_piece_wtf.lower()
                couleur_piece_wtf = form.couleur_piece_wtf.data
                couleur_piece = couleur_piece_wtf.lower()
                valeurs_insertion_dictionnaire = {
                                                    "value_intitule_num_serie_piece": num_serie_piece,
                                                    "value_intitule_couleur_piece": couleur_piece
                                                }
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_piece = """INSERT INTO `t_piece` (`num_serie_pi`, `couleur_piece`) VALUES (%(value_intitule_num_serie_piece)s,%(value_intitule_couleur_piece)s); """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_piece, valeurs_insertion_dictionnaire)
#(NULL,%(value_intitule_genre)s)
                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('pieces_afficher', order_by='DESC', id_piece_sel=0))

        except Exception as Exception_pieces_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{pieces_ajouter_wtf.__name__} ; "
                                            f"{Exception_pieces_ajouter_wtf}")

    return render_template("pieces/pieces_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update
    
    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "genres/genre_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""



@app.route("/piece_update", methods=['GET', 'POST'])
def piece_update_wtf():

        # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"

        id_piece_update = request.values['id_piece_btn_edit_html']

        # Objet formulaire pour l'UPDATE

        form_update = FormWTFUpdatePiece()

        try:

            print(" on submit ", form_update.validate_on_submit())

            if form_update.validate_on_submit():

                # Récupèrer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".

                # Puis la convertir en lettres minuscules.

                num_serie_piece_update = form_update.num_serie_piece_update_wtf.data

                # name_genre_update = name_genre_update.lower()

                couleur_piece_update = form_update.couleur_piece_update_wtf.data

                valeur_update_dictionnaire = {

                    "value_id_piece": id_piece_update,

                    "value_num_serie_piece": num_serie_piece_update,

                    "value_couleur_piece": couleur_piece_update

                }

                print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

                str_sql_update_intitulepiece = """UPDATE t_piece SET num_serie_pi=%(value_num_serie_piece)s, couleur_piece=%(value_couleur_piece)s WHERE id_piece=%(value_id_piece)s"""

                with DBconnection() as mconn_bd:

                    mconn_bd.execute(str_sql_update_intitulepiece, valeur_update_dictionnaire)

                flash(f"Donnée mise à jour !!", "success")

                print(f"Donnée mise à jour !!")

                # afficher et constater que la donnée est mise à jour.

                # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"

                return redirect(url_for('pieces_afficher', order_by="ASC", id_piece_sel=id_piece_update))

            elif request.method == "GET":

                # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"

                str_sql_id_piece = "SELECT id_piece, num_serie_pi, couleur_piece FROM t_piece WHERE id_piece=%(value_id_piece)s"

                valeur_select_dictionnaire = {"value_id_piece": id_piece_update}

                with DBconnection() as mybd_conn:

                    mybd_conn.execute(str_sql_id_piece, valeur_select_dictionnaire)

                # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE

                data_nom_genre = mybd_conn.fetchone()

                print("data_num_serie_piece ", data_nom_genre, " type ", type(data_nom_genre), " piece ",

                      data_nom_genre["num_serie_pi"])

                # Afficher la valeur sélectionnée dans les champs du formulaire "genre_update_wtf.html"

                form_update.num_serie_piece_update_wtf.data = data_nom_genre["num_serie_pi"]

                form_update.couleur_piece_update_wtf.data = data_nom_genre["couleur_piece"]


        except Exception as Exception_piece_update_wtf:

            raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "

                                          f"{piece_update_wtf.__name__} ; "

                                          f"{Exception_piece_update_wtf}")

        return render_template("pieces/piece_update_wtf.html", form_update=form_update)




"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "genres/genre_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/piece_delete", methods=['GET', 'POST'])
def piece_delete_wtf():
    data_films_attribue_piece_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_genre"
    id_piece_delete = request.values['id_piece_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeletePiece()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("piece_afficher", order_by="ASC", id_piece_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "genres/genre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_genre_delete = session['data_films_attribue_genre_delete']
                print("data_films_attribue_genre_delete ", data_films_attribue_genre_delete)

                flash(f"Effacer la piece de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_piece": id_piece_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_piece_client = """DELETE FROM t_client_acheter_piece WHERE fk_piece=%(value_id_piece)s"""
                str_sql_delete_entrepot_piece = """DELETE FROM t_entrepot_reprendre_piece WHERE fk_piece=%(value_id_piece)s"""
                str_sql_delete_fournisseur_piece = """DELETE FROM t_fournisseur_envoyer_piece WHERE fk_piece=%(value_id_piece)s"""
                str_sql_delete_piece_entrepot = """DELETE FROM t_piece_deposer_entrepot WHERE fk_piece=%(value_id_piece)s"""
                str_sql_delete_idpiece = """DELETE FROM t_piece WHERE id_piece=%(value_id_piece)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_piece_client, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_entrepot_piece, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_fournisseur_piece, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_piece_entrepot, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idpiece, valeur_delete_dictionnaire)

                flash(f"Piece définitivement effacé !!", "success")
                print(f"Piece définitivement effacé !!")

                # afficher les données
                return redirect(url_for('pieces_afficher', order_by="ASC", id_piece_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_piece": id_piece_delete}
            print(id_piece_delete, type(id_piece_delete))

            # Requête qui affiche tous les films_genres qui ont le genre que l'utilisateur veut effacer
            str_sql_genres_films_delete = """SELECT * FROM t_piece e1
                                                left JOIN t_client_acheter_piece e2 ON e1.id_piece = e2.fk_piece
                                                left JOIN t_client e3 ON e2.fk_client = e3.id_client
                                                ORDER BY e1.num_serie_pi = %(value_id_piece)s;"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
                data_films_attribue_genre_delete = mydb_conn.fetchall()
                print("data_films_attribue_genre_delete...", data_films_attribue_genre_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "genres/genre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

                # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
                str_sql_id_genre = "SELECT id_piece, num_serie_pi FROM t_piece WHERE id_piece = %(value_id_piece)s"

                mydb_conn.execute(str_sql_id_genre, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
                data_num_serie_piece = mydb_conn.fetchone()
                print("data_num_serie_piece ", data_num_serie_piece, " type ", type(data_num_serie_piece), " piece ",
                      data_num_serie_piece["num_serie_pi"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "genre_delete_wtf.html"
            form_delete.num_serie_piece_delete_wtf.data = data_num_serie_piece["num_serie_pi"]

            # Le bouton pour l'action "DELETE" dans le form. "genre_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_piece_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{piece_delete_wtf.__name__} ; "
                                      f"{Exception_piece_delete_wtf}")

    return render_template("pieces/piece_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_genre_delete)