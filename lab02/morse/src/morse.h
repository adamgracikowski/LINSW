#ifndef MORSE_H
#define MORSE_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>

#include <periphery/gpio.h>

/* Morse code sequence */
#define DOT false
#define DASH true

typedef struct MorseNode
{
    bool signal;            /* type of signal (DOT | DASH) */
    struct MorseNode *next; /* next signal in sequence */
} MorseNode;

void push_back_signal(MorseNode **head, MorseNode **tail, bool signal);
void clear_sequence(MorseNode **head, MorseNode **tail);

/* Diods */
#define DIODE_PIN 27                    /* Should not require any adjustments */
#define DIODE_PATH "/dev/gpiochip0"     /* Should not require any adjustments */
#define DIODE_ON true                   /* May require some adjustments (always !DIODE_OFF) */
#define DIODE_OFF false                 /* May require some adjustments (always !DIODE_ON) */
#define MILI_TO_MICRO 1000
#define DIODE_DOT_ON_INTERVAL_MILISECONDS (400 * MILI_TO_MICRO)
#define DIODE_DASH_ON_INTERVAL_MILISECONDS (800 * MILI_TO_MICRO)
#define DIODE_EMPTY_ON_INTERVAL_MILISECONDS (200 * MILI_TO_MICRO)

void open_diode(gpio_t **diode);
void display_signal(gpio_t *diode, int sleep);
void display_dot_signal(gpio_t *diode);
void display_dash_signal(gpio_t *diode);
void display_empty_signal();
void display_morse_sequence(gpio_t *diode, MorseNode *iterator);

/* Buttons */
#define BUTTON_DOT_PIN 25                /* May require some adjustments */
#define BUTTON_DASH_PIN 10               /* May require some adjustments */
#define BUTTON_ACCEPT_PIN 17             /* May require some adjustments */
#define BUTTON_PATH "/dev/gpiochip0"     /* Should not require any adjustments */
#define MULTIPLE_POOL_TIMEOUT -1
#define BUTTON_DOT_INDEX 0
#define BUTTON_DASH_INDEX 1
#define BUTTON_ACCEPT_INDEX 2
#define DEBOUNCE_DELAY_MILISECONDS 100   /* May require some adjustments */
#define DEBOUNCE_DELAY_MICROSECONDS (DEBOUNCE_DELAY_MILISECONDS * MILI_TO_MICRO)

void close_free_button(gpio_t **button);
void open_button(gpio_t **button, int pin, const char *path);
bool has_miliseconds_passed(uint64_t start, uint64_t end, uint64_t miliseconds);
bool empty_queue(gpio_t **button, gpio_edge_t *edge, uint64_t *button_timestamp);

#endif /* MORSE_H */