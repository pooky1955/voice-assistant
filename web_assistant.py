from __future__ import print_function
import logging, os
from dragonfly import MappingRule, Key, Text, Dictation, Integer, Grammar, Function, DictList, FuncContext
from speak import speak
import sys
import dragonfly
from keyboard_assistant import keyboard_words

state = DictList("state")
state["active"] = False
class CallbackGrammar(Grammar):

    def process_recognition(self, words, results):
        print("process_recognition()")
        print(words)
        print(results)

        # Grammar rule processing should continue after this method.
        return True

    def process_recognition_other(self, words, results):
        print("process_recognition_other()")
        print(words)
        print(results)

    def process_recognition_failure(self, results):
        print("process_recognition_failure()")
        print(results)

def sleep():
    state["active"] = False

    speak("Sleeping")
    print("Going to sleep...")

def wake():
    state["active"] = True
    speak("Hi there")
    print("Waking up...")

def status():
    ACTIVE = state["active"]
    text = "I am still sleeping" if not ACTIVE else "I'm listening"
    speak(text)
    print(f"Active = {ACTIVE}")

def quit():
    print("Have a nice day.")
    speak("Have a nice day.")
    os._exit(0)



class BootRule(MappingRule):
    mapping = {
            "assistant sleep" : Function(sleep),
            "assistant wake" : Function(wake),
            "assistant status" : Function(status),
            "assistant quit please" : Function(quit),
            }


class MediaRule(MappingRule):
    mapping = {
            "louder" : Key("volumeup"),
            "quieter" : Key("volumedown"),
            "mute" : Key("volumemute"),
            "next track" : Key("tracknext"),
            "previous track" : Key("trackprev"),
            "play" : Key("playpause"),
            "pause" : Key("playpause"),
            "history back" : Key("browserback"),
            "history forward" : Key("browserforward"),
            }


keyboard_mapping = {word : Key(letter) for letter,word in keyboard_words.items()}
class KeyboardRule(MappingRule):
    mapping = keyboard_mapping


class BrowserRule(MappingRule):
    mapping = {
            "down" : Key("d"),
            "up" : Key("u"),
            "search <text>" : Key("c-t") + Text("%(text)s\n"),
            "close" : Key("x"),
            "next" : Key("],]"),
            "previous" : Key("[,["),
            "next tab" : Key("J"),
            "previous tab" : Key("K"),
            }

    extras = [
            Dictation("text"),
            Integer("n",1,100)
            ]

browserRule = BrowserRule()
mediaRule = MediaRule()
mediaRule = MediaRule()
# Call connect() now that the engine configuration is set.
engine = dragonfly.get_engine("kaldi")
engine.connect()

grammar_context = FuncContext(lambda : state["active"])
grammar = Grammar("Default grammar","This grammar contains browsing mode",context=grammar_context)

grammar.add_rule(browserRule)
grammar.add_rule(mediaRule)

grammar.load()


boot_grammar = Grammar("Grammar for starting up and down")
boot_rule = BootRule()
boot_grammar.add_rule(boot_rule)
boot_grammar.load()

keyboard_context = FuncContext(lambda : True)
keyboard_grammar = Grammar("Grammar for keyboard mode",context=keyboard_context)
keyboard_rule = KeyboardRule()
keyboard_grammar.add_rule(keyboard_rule)
keyboard_grammar.load()

speak("Hi! I am assistant")
engine.do_recognition()
