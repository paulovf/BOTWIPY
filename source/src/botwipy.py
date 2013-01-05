# coding: utf-8
# @author: Charles Tim Batista Garrocho
# @contact: charles.garrocho@gmail.com
# @copyright: (C) 2012-2013 Python Software Open Source

import re
#import time
import tweepy
import settings
import twitter, time, urllib2, json
from os import system

system('clear')

class BotAPI(tweepy.API):

    def __init__(self):
        self.RODAR = settings.RODAR

        # Adicionado as chaves no oauth.
        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(settings.OAUTH_TOKEN, settings.OAUTH_TOKEN_SECRET)
        super(BotAPI, self).__init__(auth)
                
    def get_meu_nome(self):
        return self.me().name

    def get_meus_tweets(self):
        return tweepy.Cursor(self.user_timeline).items()

    def get_amigos_tweets(self):
        return self.friends_timeline()

    def seguir_usuario(self, usuario):
        try:
            self.get_user(usuario).follow()
            return '{0} comecou a seguir {1}'.format(self.get_meu_nome(), usuario)
        except:
            return '{0} nao conseguiu seguir {1}'.format(self.get_meu_nome(), usuario)

    def verifica_tweet(self, tweet, condicao):
        usuario = re.findall(r'{0}'.format(condicao), tweet.text)
        if (len(usuario) > 0):
            return usuario[0]
        return None

    def get_followers(self):
    	try:
		#Requisição para pegar a lista de followers de um usuário.
		resp = urllib2.urlopen('http://api.twitter.com/1/followers/ids.json?screen_name=%s' % 'botwipy')

		#Carrega a lista de followers para um dicionário.
		followers = json.loads(resp.read())
		print 'Identificador -|- Nome -|- Quantidade de seguidores'
		for follower_id in followers['ids']:
			#Requisição para pegar os dados do follower. É possível requisitar até 100 usuários por vez.
			resp = urllib2.urlopen('http://api.twitter.com/1/users/lookup.json?user_id=%s' % follower_id)
			follower = json.loads(resp.read())[0]
			print follower['screen_name'], ' -|- ', follower['name'], ' -|- ', follower['followers_count']
		return followers
	except:
		print 'Erro ao obter lista de followers'
		return None
