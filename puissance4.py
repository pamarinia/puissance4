# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 17:57:54 2024

@author: polux

PUISSANCE 4
"""

import pygame
import sys

class Bloc:
    def __init__(self, column, row, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.column = column
        self.row = row
        self.sign = 0
    
    def draw(self, window, color):
        pygame.draw.rect(window, (0,0,255), (self.x, self.y, self.width, self.height))
        pygame.draw.circle(window, (150,150,150), (self.x + self.width/2, self.y + self.height/2), self.width/3)
        if self.sign == 1: #rond rouge
            pygame.draw.circle(window, (255,0,0), (self.x + self.width/2, self.y + self.height/2), self.width/3)
        elif self.sign == 2: #rond jaune
            pygame.draw.circle(window, (0,255,255), (self.x + self.width/2, self.y + self.height/2), self.width/3)

    def click(self, x_mouse, y_mouse, player_turn):
        is_click = False
        if self.x <= x_mouse <= self.x + self.width:
            if self.y <= y_mouse <= self.y + self.height:
                is_click = True
        return self.column, is_click
                

def drop_piece(playground, column, sign):
    dropped_piece = False
    if playground[0][column].sign == 0:
        row = 0
        while row < 5 and playground[row+1][column].sign == 0:
            row += 1
        playground[row][column].sign = sign
        dropped_piece = True
        if dropped_piece:
            print(sign)
            print(playground[row][column].sign)
    return dropped_piece
    
    
def test_win(playground):
    win = False
    # On check les colonnes
    for column in range(7):
        for i in range(3):
            if playground[i][column].sign == playground[i+1][column].sign == playground[i+2][column].sign == playground[i+3][column].sign and playground[i][column].sign != 0 :
                win = True
    # On check les lignes
    for row in range(6):
        for i in range(4):
            if playground[row][i].sign == playground[row][i+1].sign == playground[row][i+2].sign == playground[row][i+3].sign and playground[row][i].sign != 0 :
                win = True
    # On check les diagonales descendantes
    for row in range(3):
        for column in range(4):
            if playground[row][column].sign == playground[row+1][column+1].sign == playground[row+2][column+2].sign == playground[row+3][column+3].sign and playground[row][column].sign != 0 :
                win = True
    # On check les diagonales montantes
    for row in range(3,6):
        for column in range(4):
            if playground[row][column].sign == playground[row-1][column+1].sign == playground[row-2][column+2].sign == playground[row-3][column+3].sign and playground[row][column].sign != 0 :
                win = True
    if win:
        print('You Win !')
    return win

def new_game():
    square_width = 80
    square_height = 80
    playground = [[Bloc(column, row, 50 + (square_width)*column, 50+(square_height)*row, square_width, square_height) for column in range(7)] for row in range(6)]
    return playground



if __name__=='__main__':
    
    pygame.init()
    
    N_columns = 7
    N_rows = 6
    # Set up the screen
    screen_width = 640
    screen_height = 800
    window = pygame.display.set_mode((screen_width, screen_height))
    window.fill((150, 150, 150))

    # Définition de la police de caractères
    police = pygame.font.Font(None, 36)

    player_1_score = 0
    player_2_score = 0
    player_turn = 1  
    
    playground = new_game()
    
    # Bouton nouvelle partie
    position_bouton = pygame.Rect(400, 650, 200, 50)
    couleur_bouton = (200, 180, 100)
    couleur_texte = (255, 255, 255)
    texte_bouton = "Nouvelle Partie"
    
    run = True
    is_win = False
    while run:
        window.fill((130, 110, 90))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Obtention des coordonnées de la souris
                x_mouse, y_mouse = pygame.mouse.get_pos()
                for i in range(N_rows):
                    for j in range(N_columns):
                        column, is_click = playground[i][j].click(x_mouse, y_mouse, player_turn)
                        if is_click:
                            if drop_piece(playground, column, player_turn):
                                player_turn = (player_turn % 2) + 1
                if is_win:
                    if position_bouton.collidepoint(x_mouse, y_mouse):
                        print("Nouvelle partie démarrée!")
                        playground = new_game()
                        is_win = False
                        
        if not is_win:
            if test_win(playground):
                is_win = True
                if player_turn == 1:
                    player_2_score += 1
                    print(player_2_score)
                elif player_turn == 2:
                    player_1_score += 1
                    print(player_1_score)
        
        
        
        for i in range(6):
            for j in range(7):
                playground[i][j].draw(window, (150,140,120))
        
        # Affichage score
        surface_texte = police.render(f"Player 1 : {player_1_score} - {player_2_score} : Player 2", True, (255, 255, 255))
        window.blit(surface_texte, (100, 660))
   
    
        # Affichage du bouton
        pygame.draw.rect(window, couleur_bouton, position_bouton)
        # Affichage du texte sur le bouton
        texte_surface = police.render(texte_bouton, True, couleur_texte)
        texte_rect = texte_surface.get_rect(center=position_bouton.center)
        window.blit(texte_surface, texte_rect)
        
        pygame.display.flip() 


        