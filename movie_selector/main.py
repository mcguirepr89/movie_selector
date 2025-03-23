#!/usr/bin/env python3

import argparse
import random
import sys
import csv
import json
from collections import defaultdict
from colorama import Fore, Style, init

init(autoreset=True)

def export_results(results, output_file, total_selections):
    if output_file.endswith('.csv'):
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Movie', 'Count', 'Percentage'])
            for movie, count in results:
                percentage = (count / total_selections) * 100
                writer.writerow([movie, count, round(percentage, 2)])
    elif output_file.endswith('.json'):
        output_data = [
            {'movie': movie, 'count': count, 'percentage': round((count / total_selections) * 100, 2)}
            for movie, count in results
        ]
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=4)
    else:
        print(f"{Fore.RED}Unsupported output format! Use .csv or .json{Style.RESET_ALL}")
        sys.exit(1)

    print(f"{Fore.GREEN}Results saved to {output_file}{Style.RESET_ALL}\n")

def prompt_for_movies():
    print(f"\n{Fore.GREEN}Enter a list of movies (press Enter after each movie, type 'done' when finished):{Style.RESET_ALL}")
    movies = []
    while True:
        movie = input("> ").strip()
        if movie.lower() == 'done':
            break
        if movie:
            movies.append(movie)
    return movies

def load_movies_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.strip().startswith('-')]
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File {filename} not found!{Style.RESET_ALL}")
        sys.exit(1)

def interactive_mode():
    print(f"{Fore.BLUE}Welcome to Interactive Mode!{Style.RESET_ALL}\n")

    num_iterations = input("Number of iterations (default 10000): ").strip()
    num_iterations = int(num_iterations) if num_iterations.isdigit() else 10000

    input_method = input("Load movies from file? (y/n): ").strip().lower()
    if input_method == 'y':
        filename = input("Enter filename: ").strip()
        movies = load_movies_from_file(filename)
    else:
        movies = prompt_for_movies()

    top_n = input("Show top N results? (leave empty for all): ").strip()
    top_n = int(top_n) if top_n.isdigit() else None

    output_file = input("Output file (optional, end with .csv or .json): ").strip()
    output_file = output_file if output_file else None

    return num_iterations, movies, top_n, output_file

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", type=int, default=10000, help="Number of iterations")
    parser.add_argument("input_file", nargs="?", default=None, help="Optional input file")
    parser.add_argument("--top", type=int, default=None, help="Show top N results only")
    parser.add_argument("--output", help="Export results to CSV or JSON file")
    parser.add_argument("--interactive", action="store_true", help="Enable interactive mode")

    args = parser.parse_args()

    if args.interactive:
        num_iterations, movies, top_n, output_file = interactive_mode()
    else:
        num_iterations = args.number
        top_n = args.top
        output_file = args.output
        movies = []

        if args.input_file:
            movies = load_movies_from_file(args.input_file)
        else:
            movies = prompt_for_movies()

    if not movies:
        print(f"{Fore.RED}No movies provided! Exiting...{Style.RESET_ALL}")
        sys.exit(1)

    random.shuffle(movies)
    selections = defaultdict(int)

    for _ in range(num_iterations):
        selected_movie = random.choice(movies)
        selections[selected_movie] += 1

    print(f"\n{Fore.BLUE}Random Selection Results:{Style.RESET_ALL}\n")

    sorted_selections = sorted(selections.items(), key=lambda x: x[1], reverse=True)
    display_limit = top_n if top_n else len(sorted_selections)

    for movie, count in sorted_selections[:display_limit]:
        percentage = (count / num_iterations) * 100
        print(f" - {Fore.YELLOW}{movie}{Style.RESET_ALL}: {Fore.RED}{count}{Style.RESET_ALL} times ({Fore.GREEN}{percentage:.1f}%{Style.RESET_ALL})")

    most_selected, max_count = sorted_selections[0]
    print(f"\n{Fore.RED}**{Style.RESET_ALL}{Fore.BLUE}Most suggested movie to watch{Style.RESET_ALL}{Fore.RED}:{Style.RESET_ALL} {Fore.YELLOW}{most_selected}{Style.RESET_ALL}\n")

    if output_file:
        export_results(sorted_selections, output_file, num_iterations)

if __name__ == "__main__":
    main()
