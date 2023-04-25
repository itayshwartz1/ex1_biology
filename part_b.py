"""
Itay Shwartz 318528171
Noa Eitan 316222777

"""




import tkinter as tk
import random
import copy

from time import sleep


class Human:

    def __init__(self, s, l):
        self.exposed = 0
        self.s = s
        self.l = l
        self.infected = False

def create_gui():
    def create_grid(p, s1, s2, s3, s4, l):
        generation = l
        root = tk.Tk()
        root.geometry("1000x1000")
        root.title("Spreading Rumours")
        s1_label = tk.Label(root, text="Human percent that exposed: 0")
        s1_label.pack()
        s2_label = tk.Label(root, text="Generation: 0")
        s2_label.pack()

        canvas = tk.Canvas(root, width=700, height=620, bg='white')
        canvas.pack()

        cell_size = 5

        padding_i = 100
        padding_j = 60

        global prev_grid
        global new_grid
        global human_exposed
        global max_index
        global humans
        global gen

        humans = 0
        gen = 0
        max_index = 100
        human_exposed = 0

        prev_grid = [[None for j in range(max_index)] for i in range(max_index)]
        new_grid = [[None for j in range(max_index)] for i in range(max_index)]

        for i in range(max_index):
            for j in range(max_index):

                if 45 < i < 55 and 45 < j < 55:
                    s = 1
                elif 35 < i < 65 and 35 < j < 65:
                    s = 2
                elif 40 < i < 70 and 40 < j < 70:
                    s = 3
                else:
                    s = 4

                if random.random() < 0.6:
                    humans += 1

                    human = Human(s, 0)
                    human.infected = False
                    prev_grid[i][j] = human
                    canvas.create_rectangle(i * cell_size + padding_i, j * cell_size + padding_j, (i + 1) * cell_size + padding_i, (j + 1) * cell_size + padding_j, fill='blue')
                else:
                    prev_grid[i][j] = None
                    canvas.create_rectangle(i * cell_size + padding_i, j * cell_size + padding_j, (i + 1) * cell_size + padding_i, (j + 1) * cell_size + padding_j, fill='white')

        human = Human(1, 0)
        human.infected = True
        prev_grid[50][50] = copy.deepcopy(human)
        canvas.create_rectangle(50 * cell_size + padding_i, 50 * cell_size + padding_j, (50 + 1) * cell_size + padding_i,
                                (50 + 1) * cell_size + padding_j, fill='red')

        human.exposed += 1

        def update_grid():

            global new_grid
            global prev_grid
            global max_index
            global human_exposed
            global gen

            to_finish = True


            percentage = round( (human_exposed / humans), 5)
            s1_label.configure(text="Human percent that exposed: " + str(percentage))
            gen += 1
            s2_label.configure(text="Generation: " + str(gen))

            for i in range(0, max_index):
                for j in range(0, max_index):
                    human = copy.deepcopy(prev_grid[i][j])
                    new_grid[i][j] = copy.deepcopy(human)

                    if human:
                        tmp_s = human.s
                        # human is blue and l is 0
                        if not human.infected and human.l == 0:
                            count = 0

                            if i > 0 and j > 0 and prev_grid[i - 1][j - 1] and prev_grid[i - 1][j - 1].infected:
                                count += 1
                            if i > 0 and prev_grid[i - 1][j] and prev_grid[i - 1][j].infected:
                                count += 1
                            if i > 0 and j < max_index - 1 and prev_grid[i - 1][j + 1] and prev_grid[i - 1][j + 1].infected:
                                count += 1
                            if j > 0 and prev_grid[i][j - 1] and prev_grid[i][j - 1].infected:
                                count += 1
                            if j < max_index - 1 and prev_grid[i][j + 1] and prev_grid[i][j + 1].infected:
                                count += 1
                            if i < max_index - 1 and j > 0 and prev_grid[i + 1][j - 1] and prev_grid[i + 1][j - 1].infected:
                                count += 1
                            if i < max_index - 1 and prev_grid[i + 1][j] and prev_grid[i + 1][j].infected:
                                count += 1
                            if i < max_index - 1 and j < max_index - 1 and prev_grid[i + 1][j + 1] and prev_grid[i + 1][j + 1].infected:
                                count += 1

                            if count == 0:
                                new_grid[i][j].infected = False
                                continue

                            if count >= 2:
                               if tmp_s != 1:
                                   tmp_s -= 1


                            r = random.random()

                            if tmp_s == 1:
                                new_grid[i][j].infected = True
                            elif tmp_s == 2 and r < 2/3:
                                new_grid[i][j].infected = True
                            elif tmp_s == 3 and r < 1/3:
                                new_grid[i][j].infected = True
                            elif tmp_s == 4:
                                new_grid[i][j].infected = False
                            else:
                                new_grid[i][j].infected = False

                            if new_grid[i][j].infected:

                                if new_grid[i][j].exposed == 0:
                                    human_exposed += 1

                                new_grid[i][j].exposed += 1

                                to_finish = False
                                canvas.create_rectangle(i * cell_size + padding_i, j * cell_size + padding_j,
                                                        (i + 1) * cell_size + padding_i, (j + 1) * cell_size + padding_j, fill='red')

                        # human is red
                        elif human.infected:
                            # turning human red to blue
                            new_grid[i][j].infected = False
                            new_grid[i][j].l = generation

                            to_finish = False
                            canvas.create_rectangle(i * cell_size + padding_i, j * cell_size + padding_j,
                                                    (i + 1) * cell_size + padding_i, (j + 1) * cell_size + padding_j, fill='blue')

                        # human is blue and l > 0
                        else:
                            new_grid[i][j].l -= 1

                    # the grid in the i j location is None
                    else:
                        new_grid[i][j] = None


            prev_grid = copy.deepcopy(new_grid)
            # need to do deep copy from the new bords to the grid 0 and 1

            if to_finish:
                return

            root.after(300, update_grid) # update the canvas
            canvas.update()

        root.after(300, update_grid)
        root.mainloop()


    create_grid(0.8, 0.6, 0.2, 0.2, 0, 3)

def main():
    create_gui()

if __name__ == "__main__":
    main()