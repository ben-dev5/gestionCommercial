# Projet 1 de Gestion Commercial et Achats pour Hotêllerie Hestia Group

# Installation et initialisation projet (Django)

- Tout d'abord installez un environnement virtuel contenant python : https://docs.python.org/3/library/venv.html
- Une fois cette étape réalisé activez l'environnement (source bin/activate) et paramétrez le sur PyCharm ou tout autre IDE. Pour PyCharm : https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html
- Ensuite il faut installer Django, pour ce faire :
    - Tapez:  `python -m pip install Django`
    - Pour créer le projet:  `django-admin startproject sitename directoryname`


- Nous avons maintenant un projet crée.
  Django utilise l'architecture ci-dessous :

      * gestionCommercial/
            * manage.py
            * hestiaCrm/
                  *  __init__.py
                  *  settings.py
                  *  urls.py
                  *  asgi.py
                  *  wsgi.py
  
  - Enfin pour lancer le projet tapez: `python manage.py runserver`

- ### L'architecture de notre projet contient plusieurs apps
   Dans chaque app se situe un dossier views, templates,
   services, repositories et models.
   De tel sorte que notre architecture actuel ressemble à ceci (chaque app représente un domaine métier)
  
                      
      * gestionCommercial/
            * manage.py
            * hestiaCrm/
                  *  __init__.py
                  *  settings.py
                  *  urls.py
                  *  asgi.py
                  *  wsgi.py        
            * commons/
                  * models/
                  * repositories/
                  * services/
                  * templates/
                  * views/
            * invoicing/
                 * models/
                 * repositories/
                 * services/
                 * templates/
                 * views/
            * purchases/
                 * models/
                 * repositories/
                 * services/
                 * templates/
                 * views/
            * sales/
                 * models/
                 * repositories/
                 * services/
                 * templates/
                 * views/
            * products/
                * models/
                * repositories/
                * services/
                * templates/
                * views/
             * static/
             * tests/
                 

- ## Surcouche Repository
  Afin de ne pas faire appel directement à la BDD avec l'ORM de Django, on crée un repository, qui lui, appelle la BDD avec des fonctions définis.
  Cela nous permet de cloisonner les appels au model. De cette façon l'on aura pas besoin de changer tout le code si on passe à du FastApi par exemple.
  De plus le services permet de faire le pont entre le model et la view par exemple afin de récupérer les informations et les traiter.  

## Settings.py    
  Enfin, il suffit dans le fichier settings.py, de demander à Django de chercher un dossier templates dans tous les sous-dossiers des Apps et non seulement à la racine du projet. 
         
     
        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [BASE_DIR / 'templates'],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                    ],
                },
            },
        ]


## Test-driven development méthode
Pour la suite du projet nous choisirons d'utiliser la méthode de Test-driven development qui consiste en la rédaction de tests avant de coder les fonctionnalités elles-mêmes. 
Ainsi on commence par le dossiers tests puis on crée le service et enfin le repository, ainsi toute la chaîne est opérationel. Et depuis les models, en passant par le repo et le services on récupère via les tests les données. 


  





