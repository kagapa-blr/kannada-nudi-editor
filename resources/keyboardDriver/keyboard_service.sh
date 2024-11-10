#!/bin/bash

# Function to send Unicode Kannada characters using `xdotool`
send_unicode() {
    # Simulate keypress of the Kannada character (Unicode)
    xdotool type --clearmodifiers --delay 100 "$(printf "\\U$1")"
}

# Main loop to handle key presses and input only Kannada characters
while true; do
    read -n 1 key
    case $key in
        a) send_unicode 0C85   # Kannada vowel 'ಅ'
            ;;
        i) send_unicode 0C87   # Kannada vowel 'ಇ'
            ;;
        u) send_unicode 0C89   # Kannada vowel 'ಉ'
            ;;
        e) send_unicode 0C8E   # Kannada vowel 'ಏ'
            ;;
        o) send_unicode 0C92   # Kannada vowel 'ಓ'
            ;;
        k) send_unicode 0C95   # Kannada consonant 'ಕ'
            ;;
        g) send_unicode 0C97   # Kannada consonant 'ಗ'
            ;;
        c) send_unicode 0C9A   # Kannada consonant 'ಚ'
            ;;
        j) send_unicode 0C9C   # Kannada consonant 'ಜ'
            ;;
        t) send_unicode 0CA4   # Kannada consonant 'ಟ'
            ;;
        d) send_unicode 0CA6   # Kannada consonant 'ಡ'
            ;;
        n) send_unicode 0CA8   # Kannada consonant 'ಣ'
            ;;
        p) send_unicode 0CAA   # Kannada consonant 'ಪ'
            ;;
        b) send_unicode 0CAC   # Kannada consonant 'ಬ'
            ;;
        m) send_unicode 0CAE   # Kannada consonant 'ಮ'
            ;;
        y) send_unicode 0CAF   # Kannada consonant 'ಯ'
            ;;
        r) send_unicode 0CB0   # Kannada consonant 'ರ'
            ;;
        l) send_unicode 0CB2   # Kannada consonant 'ಲ'
            ;;
        v) send_unicode 0CB5   # Kannada consonant 'ವ'
            ;;
        s) send_unicode 0CB8   # Kannada consonant 'ಶ'
            ;;
        h) send_unicode 0CB9   # Kannada consonant 'ಹ'
            ;;
        f) send_unicode 0CCD   # Kannada vowel sign '್' (used in combination with consonants)
            ;;
        *) # Do nothing for other keys (no English letters will be typed)
            ;;
    esac
done
