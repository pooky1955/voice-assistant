from __future__ import print_function
import logging, os
from dragonfly import MappingRule, Key, Text, Dictation, Integer, Grammar, Function, DictList, FuncContext
from speak import speak
import sys
import dragonfly

state = DictList("state")
state["active"] = False

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

speak("Hi! I am assistant")
engine.do_recognition()
