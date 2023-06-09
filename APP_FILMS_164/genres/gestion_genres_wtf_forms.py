"""
    Fichier : gestion_genres_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormWTFAjouterGenres(FlaskForm):
    """
        Dans le formulaire "genres_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_client_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_client_wtf = StringField("Insérer le nom d'un client ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                   Regexp(nom_client_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])
    prenom_client_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    prenom_client_wtf = StringField("Insérer le prénom d'un client ",
                                validators=[Length(min=2, max=20, message="min 2 max 20"),
                                            Regexp(prenom_client_regexp,
                                                   message="Pas de chiffres, de caractères "
                                                           "spéciaux, "
                                                           "d'espace à double, de double "
                                                           "apostrophe, de double trait union")
                                            ])
    submit = SubmitField("Enregistrer genre")


class FormWTFUpdateGenre(FlaskForm):
    """
        Dans le formulaire "genre_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_client_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_client_update_wtf = StringField("Modifier le nom d'un client ",
                                           validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                       Regexp(nom_client_update_regexp,
                                                              message="Pas de chiffres, de "
                                                                      "caractères "
                                                                      "spéciaux, "
                                                                      "d'espace à double, de double "
                                                                      "apostrophe, de double trait "
                                                                      "union")
                                                       ])
    prenom_client_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    prenom_client_update_wtf = StringField("Modifier le prénom d'un client ",
                                           validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                       Regexp(prenom_client_update_regexp,
                                                              message="Pas de chiffres, de "
                                                                      "caractères "
                                                                      "spéciaux, "
                                                                      "d'espace à double, de double "
                                                                      "apostrophe, de double trait "
                                                                      "union")
                                                       ])
    #date_genre_wtf_essai = DateField("Essai date", validators=[InputRequired("Date obligatoire"),
                                                               #DataRequired("Date non valide")])
    submit = SubmitField("Update genre")


class FormWTFDeleteGenre(FlaskForm):
    """
        Dans le formulaire "genre_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_client_delete_wtf = StringField("Effacer le client avec le nom :")
    prenom_client_delete_wtf = StringField("et le prénom :")
    submit_btn_del = SubmitField("Effacer client")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
