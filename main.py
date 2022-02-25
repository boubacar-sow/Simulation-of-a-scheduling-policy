#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Boubacar Sow - Maxime Delight-Schuchmann
# Created Date: Fri February 25 10:25:00  2022
# Copyright: Copyright 2022, simulation of a scheduling policy
# =============================================================================
"""The Module Has Been Build for scheduling simulation"""
# =============================================================================

import threading
from scheduler import *


def menu():
    # Display a menu, return a choice
    print("[1] Ajouter processus")
    print("[2] Supprimer processus")
    print("[3] Réinitialiser processus")
    print("[4] Lancer")
    choice = int(input("\nQue voulez-vous faire ? "))
    return choice


def menu_create_process():
    # Display for creating the process, return a new Process
    p_name = input("Nom de processus: ") or "p"
    p_priority = int(input("Priorité: ")) or 0
    p_nb_instruction_calcul = int(input("Nombre d'instructions de calcul: ")) or 9
    p_nb_instructions_in_out = int(input("Nombre d'instructions d'entrée et sortie ")) or 1
    p_nb_cycle_before_init = int(input("Nombre de cycle: ")) or 2
    p_nb_thread = int(input("Nombre de thread: ")) or 2
    return Process(p_name, p_priority, p_nb_instruction_calcul, p_nb_instructions_in_out, p_nb_cycle_before_init,
                   p_nb_thread)


def menu_delete_process(process_list):
    # Takes a list of processes, asks for a process name and deletes the process from the list
    if len(process_list) > 0:
        p_name = input("Nom du processus: ")
        for p in process_list:
            if p.name == p_name:
                del p
                print(p_name, "supprimé")
                exit(0)
        print("Processus inexistant")
    else:
        print("Aucun processus")
    exit(0)


def main():
    # Main program
    validate = False
    process = []
    while not validate:
        choice = menu()
        if choice == 1:
            process.append(menu_create_process())
        elif choice == 2:
            process.append(menu_delete_process())
        elif choice == 3:
            pass
        elif choice == 4:
            validate = True
    queue = Queue(process)
    generate_table(queue.list_process)
    policy = int(input("Votre politique d'ordonnancement PP(1)/PAPS(2): "))
    queue.launch(policy)


if __name__ == '__main__':
    thread = threading.Thread(target=main)
    thread.start()
    thread.join()
