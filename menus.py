class Menu():
    def __init__(self, prompt, options = [], default = 0):
        self.prompt = prompt
        self.options = options
        self.default = default

    def display_prompt(self):
        if len(self.options) == 2:
            if self.default == 0:
                print("%s [%s/%s]" % (self.prompt, self.options[self.default].capitalize(), self.options[1]), end = ': ')

            else:
                print("%s [%s/%s]" % (self.prompt, self.options[0], self.options[self.default].capitalize()), end = ': ')

            res = input()
            if res:
                return res
            
            else:
                return self.options[self.default]

        else:
            print("%s \n" % self.prompt)
            selection_index = 1
            for opt in self.options:
                print("%d. %s" % (selection_index, opt))
                selection_index += 1

            print("[1 - %d]" % len(self.options), end = ': ')
            res = input()
            return self.options[int(res) - 1]

if __name__ == "__main__":
    menu1 = Menu("Continue?", ['y', 'n'])
    print(menu1.display_prompt())
    menu2 = Menu("Adventurer, choose your action!", ['Attack', 'Magic', 'Item', 'Escape'])
    print(menu2.display_prompt())
    menu3 = Menu("Exit?", ['y', 'n'], 1)
    print(menu3.display_prompt())
    