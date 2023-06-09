"""
    Fichier : gestion_genres_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF

    But : Essayer un formulaire avec WTForms
"""

from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Regexp


class MonPremierWTForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(message="Mot de passe indispensable !")])

    nom_client_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_client_wtf = StringField("Insérer le nom d'un client ",
                                 validators=[Length(min=2, max=20, message="min 2 max 20"),
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

    case_cocher_npc = BooleanField('Ne pas cliquer')

    submit = SubmitField('Ok !')
