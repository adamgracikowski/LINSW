#include "morse.h"

int main()
{
    MorseNode *morse_sequence_head = NULL, *morse_sequence_tail = NULL;

    gpio_t *dot = NULL, *dash = NULL, *confirm = NULL, *diode = NULL;
    
    open_button(&dot, BUTTON_DOT_PIN, BUTTON_PATH);
    open_button(&dash, BUTTON_DASH_PIN, BUTTON_PATH);
    open_button(&confirm, BUTTON_CONFIRM_PIN, BUTTON_PATH);
    
    open_diode(&diode);
    
    gpio_t *buttons[] = { dot, dash, confirm };
    bool buttons_ready[] = { false, false, false };
    size_t buttons_count = sizeof(buttons) / sizeof(gpio_t *);
    
    while(true){
        int buttons_ready_count = 0;

        buttons_ready_count = gpio_poll_multiple(
            buttons, 
            buttons_count, 
            MULTIPLE_POOL_TIMEOUT, 
            buttons_ready
        );

        if(buttons_ready_count < 0){
            fprintf(stderr, "gpio_poll_multiple(): error code %d\n", buttons_ready_count);
            exit(EXIT_FAILURE);
        }
        else if (buttons_ready_count == 0) {
            printf("Timeout has occurred, no morse signals detected, finishing execution...\n");
            goto cleanup;
        }

        int clicked = BUTTON_CONFIRM_INDEX;
        for(int i = 0; i < buttons_count; ++i){
            if(buttons_ready[i]){
                clicked = i;
            }
            buttons_ready[i] = false;
        }

        if(clicked == BUTTON_CONFIRM_INDEX){
            printf(": CONFIRM registered.\n");

            if(morse_sequence_head == NULL){
                printf("Stop conditions satisfied, finishing execution...\n");
                goto cleanup;
            }

            display_morse_sequence(diode, morse_sequence_head);
            clear_sequence(&morse_sequence_head, &morse_sequence_tail);
        }
        else if(clicked == BUTTON_DOT_INDEX){
            printf(": DOT registered.\n");
            push_back_signal(&morse_sequence_head, &morse_sequence_tail, DOT);
        }
        else {
            printf(": DASH registered.\n");
            push_back_signal(&morse_sequence_head, &morse_sequence_tail, DASH);
        }

        usleep(DEBOUNCE_DELAY_MILISECONDS);
    }
cleanup:
    close_free_button(&dot);
    close_free_button(&dash);
    close_free_button(&confirm);

    close_free_button(&diode);

    clear_sequence(&morse_sequence_head, &morse_sequence_tail);

    return EXIT_SUCCESS;
}