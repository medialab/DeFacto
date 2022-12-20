import os
import pickle
import unittest
import json
from tqdm.auto import tqdm
from ural import is_url

from fetch import fetch_results, FetchResult
from youtube_tools import youtube_enrich, youtube_cache_filepath, temp_cache_filepath
import concurrent.futures

facebook_post = {
            "id": "Medias/Factuel/Fact-checks/Le-canular-du-transport-electrique-attention-a-cette-video-virale-sur-des-scooters-abandonnes",
            "title": "\"Le canular du transport \u00e9lectrique\" : attention \u00e0 cette vid\u00e9o virale sur des scooters \"abandonn\u00e9s\"",
            "link": "https://defacto-observatoire.fr/Medias/Factuel/Fact-checks/Le-canular-du-transport-electrique-attention-a-cette-video-virale-sur-des-scooters-abandonnes/",
            "channel": {
                "id": "Medias/Factuel",
                "name": "Factuel - AFP",
                "url": "https://factuel.afp.com/"
            },
            "chapeau": "<p>Une vid\u00e9o montrant des milliers de scooters align\u00e9s dans un terrain vague a fait le tour des r\u00e9seaux sociaux, dans des publications expliquant que ces engins \"en fin de vie\" auraient \u00e9t\u00e9 \"abandonn\u00e9s\" car leur batterie ne pourrait \u00eatre recycl\u00e9e. Ces images ont suscit\u00e9 la col\u00e8re d'internautes, ironisant sur le caract\u00e8re peu \u00e9cologique de ces v\u00e9hicules \u00e9lectriques, certains assurant que les images ont \u00e9t\u00e9 film\u00e9es en France. Mais ces images ont \u00e9t\u00e9 tourn\u00e9es en Chine. La soci\u00e9t\u00e9 commercialisant ces scooters, Meituan, assure \u00e0 l'AFP avoir lou\u00e9 le parking pour stocker \"temporairement\" certains de ses v\u00e9hicules en raison de conditions m\u00e9t\u00e9orologiques ou de restrictions des autorit\u00e9s locales sur le nombre de deux-roues en libre-service autoris\u00e9s \u00e0 circuler. En France, le recyclage de trottinettes, v\u00e9los ou scooters \u00e9lectriques et de leur batterie, encadr\u00e9 par l'UE, est obligatoire et contr\u00f4l\u00e9, ont expliqu\u00e9 deux \u00e9co-organismes \u00e0 l'AFP.</p>",
            "published": "2022-12-19T11:44:59.83+01:00",
            "authors": "Juliette MANSOUR, AFP Australie, AFP France",
            "themes": [
                "Environnement",
                "Politique"
            ],
            "tags": [
                "France"
            ],
            "medias": [
                {
                    "url": "https://defacto-observatoire.fr/download/Medias/Factuel/Fact-checks/Le-canular-du-transport-electrique-attention-a-cette-video-virale-sur-des-scooters-abandonnes/WebHome/24c269246dd80a4c481345e2e3364678bc42b075-ipad.jpg?rev=1.1"
                }
            ],
            "claim-review": {
                "@context": "https://schema.org",
                "@type": "ClaimReview",
                "url": "https://defacto-observatoire.fr/Medias/Factuel/Fact-checks/Le-canular-du-transport-electrique-attention-a-cette-video-virale-sur-des-scooters-abandonnes/",
                "datePublished": "2022-12-19T11:44:59.83+01:00",
                "author": {
                    "type": "Organization",
                    "name": "Juliette MANSOUR, AFP Australie, AFP France"
                },
                "claimReviewed": "Cette vid\u00e9o montre des scooters \u00e9lectriques abandonn\u00e9s car leur batterie ne peut pas \u00eatre recyl\u00e9e",
                "itemReviewed": {
                    "@type": "Claim",
                    "author": {
                        "@type": "Person",
                        "name": "Sources multiples"
                    },
                    "datePublished": "2022-11-30T00:00:00.00+01:00",
                    "appearance": {
                        "url": "https://www.facebook.com/koko.korinne/posts/pfbid0DghvZp4Ee5uCuEuqqzdhgL2Hux4znLx8kQauy2YcbmmE1t4f1K2j69iPbYvpNFF1l",
                        "headline": ""
                    }
                },
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": "2",
                    "bestRating": "5",
                    "worstRating": "1",
                    "alternateName": "Trompeur"
                }
            },
}

twitter_messy = {
                "id": "Medias/Factuel/Fact-checks/Non-des-brigades-de-la-mort-n-ont-pas-ete-envoyees-dans-des-EHPAD-pour-euthanasier-les-personnes-agees-avec-du-Rivotril",
                "title": "Non, des \"brigades de la mort\" n'ont pas \u00e9t\u00e9 envoy\u00e9es dans des EHPAD pour \"euthanasier\" les personnes \u00e2g\u00e9es avec du Rivotril",
                "link": "https://defacto-observatoire.fr/Medias/Factuel/Fact-checks/Non-des-brigades-de-la-mort-n-ont-pas-ete-envoyees-dans-des-EHPAD-pour-euthanasier-les-personnes-agees-avec-du-Rivotril/",
                "channel": {
                    "id": "Medias/Factuel",
                    "name": "Factuel - AFP",
                    "url": "https://factuel.afp.com/"
                },
                "chapeau": "<p>Au d\u00e9but de la crise sanitaire, au printemps 2020, un d\u00e9cret a simplifi\u00e9 la d\u00e9livrance du Rivotril (clonaz\u00e9pam), m\u00e9dicament utilis\u00e9 notamment pour les soins palliatifs. Il s'agissait \u00e0 l'\u00e9poque de pallier le manque d'un autre m\u00e9dicament, l'Hypnovel (midazolam). Les deux mol\u00e9cules ont le m\u00eame but : endormir profond\u00e9ment le patient pour qu'il ne souffre pas, jusqu'\u00e0 son d\u00e9c\u00e8s. Dans le cadre du Covid-19, il s'agissait en particulier d'\u00e9viter que des personnes \u00e2g\u00e9es malades meurent asphyxi\u00e9es. En 2020 d\u00e9j\u00e0, de nombreuses publications sur les r\u00e9seaux sociaux avaient affirm\u00e9 -\u00e0 tort- que le gouvernement avait ainsi autoris\u00e9 l'euthanasie des personnes \u00e2g\u00e9es. Ces accusations ont aussi \u00e9t\u00e9 r\u00e9cemment relay\u00e9es par des \u00e9lus. Depuis fin novembre, une vid\u00e9o intitul\u00e9e \"<em>Quand des brigades de la mort ont inject\u00e9 du Rivotril</em>\" a fait encore ressurgir ces accusations. Mais comme l'ont expliqu\u00e9 plusieurs m\u00e9decins g\u00e9riatres et sp\u00e9cialistes de la fin de vie, administrer du Rivotril ne provoque pas le d\u00e9c\u00e8s. A ce jour, l'euthanasie est interdite en France.</p>",
                "published": "2022-12-06T13:34:05.05+01:00",
                "authors": "AFP France",
                "themes": [
                    "Politique",
                    "Sant\u00e9",
                    "Soci\u00e9t\u00e9"
                ],
                "tags": [
                    "France",
                    "Covid-19"
                ],
                "medias": [
                    {
                        "url": "https://defacto-observatoire.fr/download/Medias/Factuel/Fact-checks/Non-des-brigades-de-la-mort-n-ont-pas-ete-envoyees-dans-des-EHPAD-pour-euthanasier-les-personnes-agees-avec-du-Rivotril/WebHome/fcf8e2f83922f7724d73bd57598ec546790eadaf-ipad.jpg?rev=1.1"
                    }
                ],
                "claim-review": {
                    "@context": "https://schema.org",
                    "@type": "ClaimReview",
                    "url": "https://defacto-observatoire.fr/Medias/Factuel/Fact-checks/Non-des-brigades-de-la-mort-n-ont-pas-ete-envoyees-dans-des-EHPAD-pour-euthanasier-les-personnes-agees-avec-du-Rivotril/",
                    "datePublished": "2022-12-06T13:34:05.05+01:00",
                    "author": {
                        "type": "Organization",
                        "name": "AFP France"
                    },
                    "claimReviewed": "Le Rivotril a \u00e9t\u00e9 utilis\u00e9 pour euthanasier des personnes \u00e2g\u00e9es",
                    "itemReviewed": {
                        "@type": "Claim",
                        "author": {
                            "@type": "Person",
                            "name": "Sources multiples"
                        },
                        "datePublished": "2022-11-28T00:00:00.00+01:00",
                        "appearance": {
                            "url": "https://twitter.com/GillesWell/status/1597342670380478464?ref_src=twsrc^tfw|twcamp^tweetembed|twterm^1597342670380478464|twgr^5dd17791cad5b27b171f927e6d7307bc11bf85fd|twcon^s1_&amp;ref_url=https://www.egaliteetreconciliation.fr/Des-brigades-mobiles-ont-injecte-du-Rivotril-aux-personnes-agees-dans-les-Ehpad-70479.html&amp;fbclid=IwAR19ZhCWPyqvEU1Yp1MH9Dv3LRBZNFnVfUj8OxsEaCef0cpTeojwn8AlhnM",
                            "headline": ""
                        }
                    },
                    "reviewRating": {
                        "@type": "Rating",
                        "ratingValue": "2",
                        "bestRating": "5",
                        "worstRating": "1",
                        "alternateName": "Manque de contexte"
                    }
                },
}

twitter_clean = {
    "id": "Medias/Factuel/Fact-checks/Non-l-importante-couverture-de-neige-dans-l-hemisphere-nord-ne-signifie-pas-que-les-emissions-de-CO2-ont-diminue",
            "title": "Non, l'importante \"couverture de neige dans l'h\u00e9misph\u00e8re nord\" ne signifie pas que les \u00e9missions de CO2 ont diminu\u00e9",
            "link": "https://defacto-observatoire.fr/Medias/Factuel/Fact-checks/Non-l-importante-couverture-de-neige-dans-l-hemisphere-nord-ne-signifie-pas-que-les-emissions-de-CO2-ont-diminue/",
            "channel": {
                "id": "Medias/Factuel",
                "name": "Factuel - AFP",
                "url": "https://factuel.afp.com/"
            },
            "chapeau": "<p>Nombre d'internautes affirment, sur Twitter et Facebook, que \"la couverture de neige dans l'h\u00e9misph\u00e8re nord\" est \"\u00e0 un niveau record depuis 56 ans\". Si l'enneigement de cette partie du globe \u00e9tait en effet tr\u00e8s \u00e9lev\u00e9 mi-novembre, ils y voient un signe que le \"niveau de C02 dans l'atmosph\u00e8re\", principal facteur du r\u00e9chauffement climatique, est en baisse, et remettent donc en question l'existence de ce dernier. Mais ils \u00e9tablissent un lien erron\u00e9 entre un ph\u00e9nom\u00e8ne m\u00e9t\u00e9orologique ponctuel et des \u00e9volutions climatiques observ\u00e9es sur de\u00a0 nombreuses ann\u00e9es, comme l'expliquent plusieurs sp\u00e9cialistes du climat \u00e0 l'AFP.\u00a0 En outre, la pr\u00e9sence de CO2 dans l'atmosph\u00e8re augmente d'ann\u00e9e en ann\u00e9e, comme le montrent des mesures r\u00e9alis\u00e9es depuis 1958.</p>",
            "published": "2022-11-30T17:44:21.08+01:00",
            "authors": "Alexis ORSINI, AFP France",
            "themes": [
                "Environnement",
                "Soci\u00e9t\u00e9"
            ],
            "tags": [
                "transports",
                "ratp",
                "tarif"
            ],
            "medias": [
                {
                    "url": "https://defacto-observatoire.fr/download/Medias/Factuel/Fact-checks/Non-l-importante-couverture-de-neige-dans-l-hemisphere-nord-ne-signifie-pas-que-les-emissions-de-CO2-ont-diminue/WebHome/9cbec260a2894cf42338a54ce48b19ee455f59c8-ipad.jpg?rev=1.1"
                }
            ],
            "claim-review": {
                "@context": "https://schema.org",
                "@type": "ClaimReview",
                "url": "https://defacto-observatoire.fr/Medias/Factuel/Fact-checks/Non-l-importante-couverture-de-neige-dans-l-hemisphere-nord-ne-signifie-pas-que-les-emissions-de-CO2-ont-diminue/",
                "datePublished": "2022-11-30T17:44:21.08+01:00",
                "author": {
                    "type": "Organization",
                    "name": "Alexis ORSINI, AFP France"
                },
                "claimReviewed": "L'enneigement de l'h\u00e9misph\u00e8re nord prouve que le niveau de CO2 a diminu\u00e9",
                "itemReviewed": {
                    "@type": "Claim",
                    "author": {
                        "@type": "Person",
                        "name": "Sources multiples"
                    },
                    "datePublished": "2022-11-28T00:00:00.00+01:00",
                    "appearance": {
                        "url": "https://twitter.com/Elpis_R/status/1597168976270065664",
                        "headline": ""
                    }
                },
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": "2",
                    "bestRating": "5",
                    "worstRating": "1",
                    "alternateName": "Faux"
                }
            },
}

webpage = {
    "id": "Medias/Les-Surligneurs/Fact-checks/La-mairie-de-Paris-refuse-de-transmettre-des-notes-de-frais-a-un-journaliste-malgre-une-decision-de-justice",
            "title": "La mairie de Paris refuse de transmettre des notes de frais \u00e0 un journaliste malgr\u00e9 une d\u00e9cision de justice",
            "link": "https://defacto-observatoire.fr/Medias/Les-Surligneurs/Fact-checks/La-mairie-de-Paris-refuse-de-transmettre-des-notes-de-frais-a-un-journaliste-malgre-une-decision-de-justice/",
            "channel": {
                "id": "Medias/Les-Surligneurs",
                "name": "Les Surligneurs",
                "url": "https://lessurligneurs.eu/"
            },
            "chapeau": "<p>Les notes de frais des maires sont l\u00e9galement des documents communicables (par des copies) \u00e0 qui les demande. Reste que les moyens de pression sur l\u2019administration sont bien maigres, et que ce n\u2019est peut-\u00eatre pas par hasard.</p>",
            "published": "2022-12-08T15:24:21.24+01:00",
            "authors": "Auteur : Jean-Paul Markus, professeur de droit public, Universit\u00e9 Paris-Saclay\n\nAuteur : Vincent Couronne, docteur en droit europ\u00e9en, chercheur associ\u00e9 au centre de recherches VIP, Universit\u00e9 Paris-Saclay",
            "themes": [
                "Politique"
            ],
            "tags": [
                "politique",
                "France"
            ],
            "medias": [
                {
                    "url": "https://defacto-observatoire.fr/download/Medias/Les-Surligneurs/Fact-checks/La-mairie-de-Paris-refuse-de-transmettre-des-notes-de-frais-a-un-journaliste-malgre-une-decision-de-justice/WebHome/hidalgo-600x400.png?rev=1.1"
                }
            ],
            "claim-review": {
                "@context": "https://schema.org",
                "@type": "ClaimReview",
                "url": "https://defacto-observatoire.fr/Medias/Les-Surligneurs/Fact-checks/La-mairie-de-Paris-refuse-de-transmettre-des-notes-de-frais-a-un-journaliste-malgre-une-decision-de-justice/",
                "datePublished": "2022-12-08T15:24:21.24+01:00",
                "author": {
                    "type": "Organization",
                    "name": "Auteur : Jean-Paul Markus, professeur de droit public, Universit\u00e9 Paris-Saclay\n\nAuteur : Vincent Couronne, docteur en droit europ\u00e9en, chercheur associ\u00e9 au centre de recherches VIP, Universit\u00e9 Paris-Saclay"
                },
                "claimReviewed": "La mairie de Paris refuse de transmettre des notes de frais \u00e0 un journaliste malgr\u00e9 une d\u00e9cision de justice.",
                "itemReviewed": {
                    "@type": "Claim",
                    "author": {
                        "@type": "Person",
                        "name": "Atlantico"
                    },
                    "datePublished": "2022-10-14T00:00:00.00+02:00",
                    "appearance": {
                        "url": "https://atlantico.fr/article/pepite/la-mairie-de-paris-refuse-toujours-de-transmettre-les-notes-de-frais-d-anne-hidalgo-malgre-les-requetes-du-journaliste-stefan-de-vries-conseil-d-etat-avocat-association-journalisme-frais-soutien-aide",
                        "headline": ""
                    }
                },
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": "2",
                    "bestRating": "5",
                    "worstRating": "1",
                    "alternateName": "Sans doute ill\u00e9gal"
                }
            },
}

youtube_video_fr = {
    "id": "Medias/Factuel/Fact-checks/Le-vaccin-illegal-et-dangereux-quatre-fois-plus-de-morts-chez-les-vaccines-au-Royaume-Uni-attention-a-ces-propos-de-Christian-Perronne",
            "title": "Le vaccin \"ill\u00e9gal\" et dangereux, quatre fois plus de morts chez les vaccin\u00e9s au Royaume-Uni : attention \u00e0 ces propos de Christian Perronne",
            "link": "https://defacto-observatoire.fr/Medias/Factuel/Fact-checks/Le-vaccin-illegal-et-dangereux-quatre-fois-plus-de-morts-chez-les-vaccines-au-Royaume-Uni-attention-a-ces-propos-de-Christian-Perronne/",
            "channel": {
                "id": "Medias/Factuel",
                "name": "Factuel - AFP",
                "url": "https://factuel.afp.com/"
            },
            "chapeau": "<p>Le vaccin anti-Covid n'en serait pas un et serait \"totalement interdit\" en France selon \"le code de Nuremberg\", l'\u00e9pid\u00e9mie n'existerait plus dans \"tous les pays qui n'ont pas vaccin\u00e9\", les personnes vaccin\u00e9es mourraient \"quatre fois plus\" du Covid au Royaume-Uni, et les \"donn\u00e9es europ\u00e9ennes\" d\u00e9montreraient qu'il y a \"20.000 morts du vaccin\" : ces affirmations de Christian Perronne sur le plateau de CNews, tr\u00e8s relay\u00e9es sur Internet, sont trompeuses voire infond\u00e9es, selon plusieurs sp\u00e9cialistes interrog\u00e9s par l'AFP.</p>",
            "published": "2021-11-23T15:47:00.00+01:00",
            "authors": "Claire Line NASS, AFP France",
            "themes": [
                "Sant\u00e9"
            ],
            "tags": [
                "Covid-19",
                "Vaccins",
                "France"
            ],
            "medias": [
                {
                    "url": "https://defacto-observatoire.fr/download/Medias/Factuel/Fact-checks/Le-vaccin-illegal-et-dangereux-quatre-fois-plus-de-morts-chez-les-vaccines-au-Royaume-Uni-attention-a-ces-propos-de-Christian-Perronne/WebHome/ec6ed38ad43a839417b5cf8c53a3c90f.jpeg?rev=1.1"
                }
            ],
            "claim-review": {
                "@context": "https://schema.org",
                "@type": "ClaimReview",
                "url": "https://defacto-observatoire.fr/Medias/Factuel/Fact-checks/Le-vaccin-illegal-et-dangereux-quatre-fois-plus-de-morts-chez-les-vaccines-au-Royaume-Uni-attention-a-ces-propos-de-Christian-Perronne/",
                "datePublished": "2021-11-23T15:47:00.00+01:00",
                "author": {
                    "type": "Organization",
                    "name": "Claire Line NASS, AFP France"
                },
                "claimReviewed": "Les vaccins anti-Covid ne sont pas des vaccins et sont ill\u00e9gaux",
                "itemReviewed": {
                    "@type": "Claim",
                    "author": {
                        "@type": "Person",
                        "name": "Christian Perronne"
                    },
                    "datePublished": "2021-11-21T00:00:00.00+01:00",
                    "appearance": {
                        "url": "https://www.youtube.com/watch?v=bj6PcWBgVN4",
                        "headline": ""
                    }
                },
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": "2",
                    "bestRating": "5",
                    "worstRating": "1",
                    "alternateName": "Infond\u00e9, trompeur"
                }
            },
}

youtube_user = {
    "id": "Medias/Factuel/Fact-checks/Cette-video-d-Ursula-von-der-Leyen-diffusee-en-2020-ne-montre-pas-comment-economiser-de-l-eau-en-se-lavant-les-mains",
            "title": "Cette vid\u00e9o d'Ursula von der Leyen diffus\u00e9e en 2020 ne montre pas comment \u00e9conomiser de l'eau en se lavant les mains",
            "link": "https://defacto-observatoire.fr/Medias/Factuel/Fact-checks/Cette-video-d-Ursula-von-der-Leyen-diffusee-en-2020-ne-montre-pas-comment-economiser-de-l-eau-en-se-lavant-les-mains/",
            "channel": {
                "id": "Medias/Factuel",
                "name": "Factuel - AFP",
                "url": "https://factuel.afp.com/"
            },
            "chapeau": "<p>Une vid\u00e9o montrant la pr\u00e9sidente de la Commission europ\u00e9enne\u00a0Ursula von der Leyen se laver les mains a \u00e9t\u00e9 mise en ligne en 2020 dans le cadre d'une campagne de pr\u00e9vention contre le Covid-19 et non pour montrer comment \u00e9conomiser de l'eau, contrairement \u00e0 ce qu'affirment des publications relay\u00e9es plusieurs milliers de fois sur les r\u00e9seaux sociaux d\u00e9but septembre. Elle a \u00e9t\u00e9 r\u00e9alis\u00e9e pour promouvoir un lavage efficace des mains, au d\u00e9but de la pand\u00e9mie de coronavirus.</p>",
            "published": "2022-09-19T17:57:27.47+02:00",
            "authors": "Marie GENRIES, MAJA CZARNECKA, AFP Pologne",
            "themes": [
                "Politique",
                "Sant\u00e9",
                "Soci\u00e9t\u00e9"
            ],
            "tags": [
                "Covid-19"
            ],
            "medias": [
                {
                    "url": "https://defacto-observatoire.fr/download/Medias/Factuel/Fact-checks/Cette-video-d-Ursula-von-der-Leyen-diffusee-en-2020-ne-montre-pas-comment-economiser-de-l-eau-en-se-lavant-les-mains/WebHome/181745cc04445dc79fa81005d4abea043ce1812a-ipad.jpg?rev=1.1"
                }
            ],
            "claim-review": {
                "@context": "https://schema.org",
                "@type": "ClaimReview",
                "url": "https://defacto-observatoire.fr/Medias/Factuel/Fact-checks/Cette-video-d-Ursula-von-der-Leyen-diffusee-en-2020-ne-montre-pas-comment-economiser-de-l-eau-en-se-lavant-les-mains/",
                "datePublished": "2022-09-19T17:57:27.47+02:00",
                "author": {
                    "type": "Organization",
                    "name": "Marie GENRIES, MAJA CZARNECKA, AFP Pologne"
                },
                "claimReviewed": "Cette vid\u00e9o montre la pr\u00e9sidente de la Commission europ\u00e9enne Ursula Von der Leyen montrer comment se laver les mains sans gaspiller d'eau",
                "itemReviewed": {
                    "@type": "Claim",
                    "author": {
                        "@type": "Person",
                        "name": "Sources multiples"
                    },
                    "datePublished": "2022-09-07T00:00:00.00+02:00",
                    "appearance": {
                        "url": "https://www.youtube.com/user/CABAtransport",
                        "headline": ""
                    }
                },
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": "1",
                    "bestRating": "5",
                    "worstRating": "1",
                    "alternateName": "Faux"
                }
            },
}

youtube_channel = {
    "id": "Medias/Factuel/Fact-checks/Cette-video-d-Ursula-von-der-Leyen-diffusee-en-2020-ne-montre-pas-comment-economiser-de-l-eau-en-se-lavant-les-mains",
            "title": "Cette vid\u00e9o d'Ursula von der Leyen diffus\u00e9e en 2020 ne montre pas comment \u00e9conomiser de l'eau en se lavant les mains",
            "link": "https://defacto-observatoire.fr/Medias/Factuel/Fact-checks/Cette-video-d-Ursula-von-der-Leyen-diffusee-en-2020-ne-montre-pas-comment-economiser-de-l-eau-en-se-lavant-les-mains/",
            "channel": {
                "id": "Medias/Factuel",
                "name": "Factuel - AFP",
                "url": "https://factuel.afp.com/"
            },
            "chapeau": "<p>Une vid\u00e9o montrant la pr\u00e9sidente de la Commission europ\u00e9enne\u00a0Ursula von der Leyen se laver les mains a \u00e9t\u00e9 mise en ligne en 2020 dans le cadre d'une campagne de pr\u00e9vention contre le Covid-19 et non pour montrer comment \u00e9conomiser de l'eau, contrairement \u00e0 ce qu'affirment des publications relay\u00e9es plusieurs milliers de fois sur les r\u00e9seaux sociaux d\u00e9but septembre. Elle a \u00e9t\u00e9 r\u00e9alis\u00e9e pour promouvoir un lavage efficace des mains, au d\u00e9but de la pand\u00e9mie de coronavirus.</p>",
            "published": "2022-09-19T17:57:27.47+02:00",
            "authors": "Marie GENRIES, MAJA CZARNECKA, AFP Pologne",
            "themes": [
                "Politique",
                "Sant\u00e9",
                "Soci\u00e9t\u00e9"
            ],
            "tags": [
                "Covid-19"
            ],
            "medias": [
                {
                    "url": "https://defacto-observatoire.fr/download/Medias/Factuel/Fact-checks/Cette-video-d-Ursula-von-der-Leyen-diffusee-en-2020-ne-montre-pas-comment-economiser-de-l-eau-en-se-lavant-les-mains/WebHome/181745cc04445dc79fa81005d4abea043ce1812a-ipad.jpg?rev=1.1"
                }
            ],
            "claim-review": {
                "@context": "https://schema.org",
                "@type": "ClaimReview",
                "url": "https://defacto-observatoire.fr/Medias/Factuel/Fact-checks/Cette-video-d-Ursula-von-der-Leyen-diffusee-en-2020-ne-montre-pas-comment-economiser-de-l-eau-en-se-lavant-les-mains/",
                "datePublished": "2022-09-19T17:57:27.47+02:00",
                "author": {
                    "type": "Organization",
                    "name": "Marie GENRIES, MAJA CZARNECKA, AFP Pologne"
                },
                "claimReviewed": "Cette vid\u00e9o montre la pr\u00e9sidente de la Commission europ\u00e9enne Ursula Von der Leyen montrer comment se laver les mains sans gaspiller d'eau",
                "itemReviewed": {
                    "@type": "Claim",
                    "author": {
                        "@type": "Person",
                        "name": "Sources multiples"
                    },
                    "datePublished": "2022-09-07T00:00:00.00+02:00",
                    "appearance": {
                        "url": "https://www.youtube.com/@LofiGirl",
                        "headline": ""
                    }
                },
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": "1",
                    "bestRating": "5",
                    "worstRating": "1",
                    "alternateName": "Faux"
                }
            },
}



data = [youtube_video_fr, youtube_channel, youtube_user]

dfclaim_with_url = [claim_url_pair for claim_url_pair in 
            [
                {"claim":claim, 
                "url":claim.get(\
                    "claim-review",{}).get(\
                        "itemReviewed",{}).get(\
                            "appearance",{}).get(\
                                "url")} 
                for claim in data
            ] 
        if claim_url_pair["url"] and is_url(claim_url_pair["url"])]


def test():
    results:list[FetchResult] = fetch_results(dfclaim_with_url)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(youtube_enrich, results), total=len(results), desc="Multiprocess YouTube URLs"))

if __name__ == "__main__":
    test()