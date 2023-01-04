# DeFacto
Tools to enrich De Facto's database

# How To

1. Clone the repository and install the requirements (`./requirements.txt`) in a virtual environment.

2. Create and configure the JSON (`./config.json`), where the "endpoint" is the URI to De Facto's database.
```python
{
    "endpoint": "XXXXXX",
    "crowdtangle":{
        "token": "XXXXXX",
        "rate_limit": 50
    },
    "twitter":{
        "key": "XXXXXX",
        "secret_key": "XXXXXX",
        "token": "XXXXXX-XXXXXX",
        "secret_token": "XXXXXX"
    },
    "youtube":{
        "key": "XXXXXX"
    }
}
```

3. Get and format data from the database in preparation for the enrichment, which is designed to take any database's data when formatted properly.
```shell
$ python data/defacto/format.py
```

4. Run the enrichment and output a new JSON to replace that which De Facto's API sent originally.
```shell
$ python src/main.py data/defacto.json
```

# Output
In the `appearance` for reviewed claims with a valid URL, the following enrichment will be added:
- YouTube Video
```python
"appearance": {
                        "url": "https://www.youtube.com/watch?v=iBBtuSOEQC0",
                        "headline": "",
                        "domain": "youtube.com",
                        "domain-specific": {
                            "video_id": "iBBtuSOEQC0",
                            "channel_id": "UCjTbZBXEw-gplUAnMXLYHpg",
                            "channel_name": "Éric Zemmour",
                            "video_title": "Éric Zemmour : Discours de Villepinte",
                            "video_description": "Voici en intégralité mon discours à Villepinte !1️⃣ Likez la vidéo, Abonnez-vous à ma chaîne YouTube en cliquant sur le bouton « s'abonner » et sur la cloche...",
                            "video_views": "360765",
                            "video_published": "2021-12-06"
                        }
                    }
```

---

- Tweet
```python
"appearance": {
                        "url": "http://twitter.com/chadaly5/status/1464562608443375617",
                        "headline": "",
                        "domain": "twitter.com",
                        "text": "SELON DR. SHANKARA CHETTY : « LA PROTÉINE SPIKE EST LE PIRE POISON JAMAIS CRÉÉ PAR L’HOMME » \nDr Shankara Chetty, d'Afrique du Sud, est un expert mondial de la science et du traitement du covid 19. \n\nIl a traité plus de 7000 patients, sans décès ni hospitalisation. https://twitter.com/chadaly5/status/1464562608443375617/video/1",
                        "domain-specific": {
                            "tweet_id": "1464562608443375617",
                            "user_screen_name": "chadaly5",
                            "normalized_tweet_payload": {
                                "id": "1464562608443375617",
                                "local_time": "2021-11-27T11:51:50",
                                "timestamp_utc": 1638013910,
                                "text": "SELON DR. SHANKARA CHETTY : « LA PROTÉINE SPIKE EST LE PIRE POISON JAMAIS CRÉÉ PAR L’HOMME » \nDr Shankara Chetty, d'Afrique du Sud, est un expert mondial de la science et du traitement du covid 19. \n\nIl a traité plus de 7000 patients, sans décès ni hospitalisation. https://twitter.com/chadaly5/status/1464562608443375617/video/1",
                                "url": "https://twitter.com/chadaly5/status/1464562608443375617",
                                "hashtags": [],
                                "mentioned_names": [],
                                "mentioned_ids": [],
                                "collection_time": "2022-12-20T17:54:33.110626",
                                "user_id": "1378741847581921283",
                                "user_screen_name": "chadaly5",
                                "user_name": "Cha Daly🥕🥕🧠🤌",
                                "user_image": "https://pbs.twimg.com/profile_images/1378754139958706177/C_ej5WHH_normal.jpg",
                                "user_url": null,
                                "user_location": null,
                                "user_verified": false,
                                "user_description": "Putain encore 5 ans !!😱 #Frexit !!!",
                                "user_tweets": 16496,
                                "user_followers": 509,
                                "user_friends": 844,
                                "user_lists": 4,
                                "user_created_at": "2021-04-04T16:10:58",
                                "user_timestamp_utc": 1617552658,
                                "possibly_sensitive": false,
                                "like_count": 19,
                                "retweet_count": 28,
                                "quote_count": 0,
                                "reply_count": 1,
                                "lang": "fr",
                                "source_name": "Twitter for iPad",
                                "links": [
                                    "https://twitter.com/chadaly5/status/1464562608443375617/video/1"
                                ],
                                "media_urls": [
                                    ""
                                ],
                                "media_files": [
                                    "1464562608443375617_"
                                ],
                                "media_types": [
                                    "video"
                                ],
                                "match_query": true,
                                "collected_via": [
                                    "api"
                                ]
                            }
                        }
                    },
```

---

- Web Page
```python
"appearance": {
                        "url": "https://www.nicematin.com/justice/le-petit-a-merite-ce-qui-lui-arrive-mais-nous-leur-fils-agresse-une-mamie-a-cannes-le-maire-retire-leur-emplacement-au-marche-812038?utm_term=Autofeed&utm_medium=Social&utm_source=Twitter#Echobox=1670015946",
                        "headline": "",
                        "domain": "nicematin.com",
                        "text": "La Ville ne \"cédera ni aux pressions, ni aux menaces\"\nContacté, le cabinet du maire confirme le retrait de l’emplacement dans la foulée des faits.\n\"On est responsable de ses enfants, nous indique-t-on d’emblée. Occuper le domaine public, c’est un droit particulier: nous avons considéré qu’il était incompatible d’accueillir les parents d’un enfant qui a commis de tels actes.\"\nPour justifier la décision municipale – prise en s’appuyant \"sur la réglementation des marchés de Cannes\" – on évoque, aussi, \"une mesure d’ordre\": \"On ne savait pas quelle allait être la réaction des gens sur le marché.\"\nUne mesure conservatoire, au départ, \"en attendant la décision de justice\". Sauf qu’entre-temps... \"Nous les avions déjà reçus, à leur demande, juste après les faits. Et avions convenu d’un nouveau rendez-vous après le passage au tribunal. Hier [jeudi 1er décembre], nous avons reçu la femme et la fille aînée et cela ne s’est pas très bien passé.\"\nCôté mairie, on évoque une \"attitude menaçante et des sous-entendus\". Ce que nient les principaux intéressés.\nFace à cela, l’emplacement, qui n’avait pas été réattribué depuis au marché de La Bocca, va l’être prochainement: \"La commission chargée de l’attribution des places va se réunir et désigner un autre bénéficiaire. Il y a beaucoup de demandes, émanant notamment de familles méritantes.\"\nLogement: le maire souhaite une expulsion\nEn conclusion: \"Le maire recevra la famille [la semaine prochaine, possiblement] mais il ne cédera ni aux pressions, ni aux menaces.\"\nDavid Lisnard portait en octobre, avec la députée LR cannoise Alexandra Martin, une proposition de loi sur la délinquance des mineurs, visant, notamment, à alourdir les sanctions – y compris vis-à-vis des familles – dans certains cas.\nPeu après l’agression, il avait, déjà, écrit au ministre de l’Intérieur, Gérald Darmanin, pour que l’excuse de minorité soit levée dans des cas aussi graves. Mais aussi pour demander la suspension immédiate \"du versement de toute aide sociale au profit des familles\".\nIl avait, enfin, contacté les bailleurs concernés pour que les familles des trois jeunes soient expulsées de leurs logements sociaux. \"Ils attendent la décision de justice pour se prononcer\", explique la Ville.\ncommentaires",
                        "domain-specific": {
                            "title": "\"Le petit a mérité ce qui lui arrive, mais nous?\" Leur fils agresse une mamie à Cannes, le maire retire leur emplacement au marché - Nice-Matin",
                            "lang": "fr"
                        }
                    },
                    "lang": "fr"
                },
```
