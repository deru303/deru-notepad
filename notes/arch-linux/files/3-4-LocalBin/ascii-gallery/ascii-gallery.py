#!/usr/bin/env python3
try:
    import os
    import sys
    import requests
    import argparse
    from bs4 import BeautifulSoup
    from colorama import Fore, Style, init as color_conversion_init


    if os.name == "nt":
        color_conversion_init(convert=True)


    def cprint(*args, color=None, bold=False):
        if bold:
            print(f"{Style.BRIGHT}", end="")
        if color:
            print(f"{color}", end="")
        print(*args, end="")
        print(f"{Style.RESET_ALL}")


    def cls():
        os.system('cls' if os.name=='nt' else 'clear')


    def get_categories(cat_url="https://www.asciiart.eu"):
        with requests.get(cat_url) as main_page:
            soup = BeautifulSoup(main_page.text, 'html.parser')
            category_links = soup.select(".directory-columns li a", href=True)
            return [(link.text, cat_url + link["href"]) for link in category_links if not link.text.endswith("@")]


    def get_arts(art_url):
        with requests.get(art_url) as main_page:
            soup = BeautifulSoup(main_page.text, 'html.parser')
            art_tags = soup.select(".border-header.border-top.p-3 pre")
            return [art.text for art in art_tags]


    def resolve_chosen_category(allowed_categories, user_input):
        if user_input.isdigit() and int(user_input) > 0:
            chosen_index = int(user_input)
            if not chosen_index > len(allowed_categories):
                return allowed_categories[chosen_index - 1]
            else:
                return None
        else:
            allowed_choices = list(map(lambda cat: cat[0].lower(), allowed_categories))
            chosen_category_name = user_input.lower()
            if not chosen_category_name not in allowed_choices:
                return allowed_categories[allowed_choices.index(chosen_category_name)]
            else:
                return None


    def resolve_chosen_arts(allowed_categories, chosen_category, chosen_subdirectory):
        chosen_category = resolve_chosen_category(allowed_categories, chosen_category)
        if chosen_category is None:
            return None
        chosen_category_name, chosen_category_url = chosen_category

        sub_directories = get_categories(chosen_category_url)
        chosen_subcategory = resolve_chosen_category(sub_directories, chosen_subdirectory)
        if chosen_subcategory is None:
            return None
        chosen_subcategory_name, chosen_subcategory_url = chosen_subcategory
        return get_arts(chosen_subcategory_url)


    def print_category_tree(categories):
        for category_index, category in enumerate(categories):
            category_name, category_url = category
            print("{}. {}".format(category_index + 1, category_name))


    def run():
        argparser = argparse.ArgumentParser(
            description="Console ascii-art fetching tool for https://www.asciiart.eu",
            epilog="Made with heart by Daniel Rogowski"
        )
        argparser.add_argument(
            "--color", dest="color", metavar="color_name",
            help="Color of displayed ascii arts",
            choices=['black', 'blue', 'cyan', 'green', 'magenta', 'red', 'white', 'yellow'],
            default="reset"
        )
        argparser.add_argument(
            "--bold", dest="bold",
            help="Should ascii art be bolded?",
            action="store_true",
            default=False
        )
        argparser.add_argument(
            "--fullscreen", dest="fullscreen",
            help="App pretends to be full screen by cleaning the console and requesting confirmation with an enter key",
            action="store_true",
            default=False
        )
        argparser.add_argument(
            nargs="*", dest="category"
        )
        args = argparser.parse_args()
        main_categories = get_categories()

        if args.fullscreen:
            cls()

        if not args.category:
            cprint("AVAILABLE CATEGORIES:", bold=True)
            print_category_tree(main_categories)
            cprint("\nTo select a specific category, use:", bold=True)
            print("ascii-gallery category_name\t(i.e. ascii-gallery Animals)")
            print("ascii-gallery category_number\t(i.e. ascii-gallery 1)")

        elif len(args.category) == 1:
            chosen_category = resolve_chosen_category(main_categories, args.category[0])
            if chosen_category is None:
                print("There is no category with such name or index.", file=sys.stderr)
                exit(1)
            chosen_category_name, chosen_category_url = chosen_category

            sub_categories = get_categories(chosen_category_url)
            cprint("LISTING AVAILABLE SUBCATEGORIES FOR CATEGORY {}:".format(chosen_category_name.upper()), bold=True)
            print_category_tree(sub_categories)
            cprint("\nTo select a specific subcategory, use:", bold=True)
            print("ascii-gallery \"{0}\" subcategory_name"
                "\t(i.e. ascii-gallery \"{0}\" \"{1}\")".format(chosen_category_name, sub_categories[0][0]))
            print("ascii-gallery \"{0}\" subcategory_number"
                "\t(i.e. ascii-gallery \"{0}\" 1)".format(chosen_category_name))

        elif len(args.category) == 2:
            ascii_arts = resolve_chosen_arts(main_categories, args.category[0], args.category[1])
            if ascii_arts == None:
                print("There is no category with such name or index.", file=sys.stderr)
                exit(1)
            
            cprint("PRINTING ALL ASCII-ARTS FOR SPECIFIED SUBCATEGORY:", bold=True)
            cmd = "ascii-gallery \"{0}\" \"{1}\" art-number\t" \
                "(i.e. ascii-gallery \"{0}\" \"{1}\" 1".format(args.category[0], args.category[1])
            print("To print only specific ascii-art, use:\n{})".format(cmd))

            for art_number, art in enumerate(ascii_arts):
                color_code = getattr(Fore, args.color.upper())
                cprint("ART NO. " + str(art_number + 1), bold=True)
                cprint(art, color=color_code, bold=args.bold)
                print("\n\n\n")

        elif len(args.category) == 3:
            ascii_arts = resolve_chosen_arts(main_categories, args.category[0], args.category[1])
            try:
                color_code = getattr(Fore, args.color.upper())
                cprint(ascii_arts[int(args.category[2]) - 1], color=color_code, bold=args.bold)
            except IndexError:
                print("There is no ascii art with such number!", file=sys.stderr)
                exit(1)
            except ValueError:
                print("You need to specify valid ascii art number!", file=sys.stderr)
                exit(1)

        else:
            print("Unrecognized number of arguments: " + str(len(args.category)), file=sys.stderr)
            exit(1)

        if args.fullscreen:
            input()
            cls()

    if __name__ == '__main__':
        run()
except KeyboardInterrupt:
    print("Got interrupt signal, exiting...")
except requests.exceptions.ConnectionError:
    print("Networking error. Check your internet connection.")
