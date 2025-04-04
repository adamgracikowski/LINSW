#include "morse.h"

/* Morse code sequence */

/* Adds a new element at the end of the sequence */
void push_back_signal(MorseNode **head, MorseNode **tail, bool signal)
{
    MorseNode *new_node = (MorseNode *)malloc(sizeof(MorseNode));
    if (!new_node)
    {
        fprintf(stderr, "push_back_signal: malloc\n");
        exit(EXIT_FAILURE);
    }

    new_node->signal = signal;
    new_node->next = NULL;

    if (*tail)
    {
        (*tail)->next = new_node;
    }
    else
    {
        *head = new_node;
    }

    *tail = new_node;
}

/* Removes all signals from the sequence*/
void clear_sequence(MorseNode **head, MorseNode **tail)
{
    MorseNode *current = *head;
    while (current)
    {
        MorseNode *next = current->next;
        free(current);
        current = next;
    }
    
    *head = NULL;
    *tail = NULL;
}

/* Diodes */
void open_diode(gpio_t **diode)
{
    if ((*diode = gpio_new()) == NULL)
    {
        fprintf(stderr, "gpio_new: Failed to allocate a GPIO handle.\n");
        exit(EXIT_FAILURE);
    }

    if (gpio_open(*diode, DIODE_PATH, DIODE_PIN, GPIO_DIR_OUT) < 0)
    {
        fprintf(stderr, "gpio_open(): %s\n", gpio_errmsg(*diode));
        gpio_free(*diode);
        exit(EXIT_FAILURE);
    }
}
void display_signal(gpio_t *diode, int sleep)
{
    printf(": DIODE ON\n");

    if (gpio_write(diode, DIODE_ON) < 0)
    {
        fprintf(stderr, "gpio_write(): %s\n", gpio_errmsg(diode));
        exit(EXIT_FAILURE);
    }

    usleep(sleep);

    printf(": DIODE OFF\n");

    if (gpio_write(diode, DIODE_OFF) < 0)
    {
        fprintf(stderr, "gpio_write(): %s\n", gpio_errmsg(diode));
        exit(EXIT_FAILURE);
    }
}
void display_dot_signal(gpio_t *diode)
{
    display_signal(diode, DIODE_DOT_ON_INTERVAL_MILISECONDS);
}
void display_dash_signal(gpio_t *diode)
{
    display_signal(diode, DIODE_DASH_ON_INTERVAL_MILISECONDS);
}
void display_empty_signal()
{
    usleep(DIODE_EMPTY_ON_INTERVAL_MILISECONDS);
}
void display_morse_sequence(gpio_t *diode, MorseNode *iterator)
{
    while (iterator != NULL)
    {
        if (iterator->signal == DOT)
            display_dot_signal(diode);
        else
            display_dash_signal(diode);
        display_empty_signal();
        iterator = iterator->next;
    }
}

/* Buttons */
void close_free_button(gpio_t **button)
{
    if(gpio_close(*button) < 0){
        fprintf(stderr, "gpio_close(): %s\n", gpio_errmsg(*button));
        gpio_free(*button);
        exit(EXIT_FAILURE);
    }

    gpio_free(*button);
}
void open_button(gpio_t **button, int pin, const char *path)
{
    if((*button = gpio_new()) == NULL){ 
        fprintf(stderr, "gpio_new: Failed to allocate a GPIO handle.\n");
        exit(EXIT_FAILURE);
    }

    if(gpio_open(*button, path, pin, GPIO_DIR_OUT) < 0){
        fprintf(stderr, "gpio_open(): %s\n", gpio_errmsg(*button));
        gpio_free(*button);
        exit(EXIT_FAILURE);
    }

    if(gpio_set_edge(*button, GPIO_EDGE_FALLING) < 0){
        fprintf(stderr, "gpio_set_edge(): %s\n", gpio_errmsg(*button));
        close_free_button(button);
        exit(EXIT_FAILURE);
    }
}