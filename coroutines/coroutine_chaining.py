#%% [markdown]
# ## Coroutine
#
# Program that demonstrates how the coroutine chaining works
#

#%% [markdown]
#First of all, we have a producer, that is not a coroutine.
#
#The producer had an parameter called `next_coroutine`; the producer only sends
#the procecced data to this coroutine, but hes not know what kind of function
#that coroutine is.


#%%
def producer(sentence: str, next_coroutine=None) -> None:
    """Split the sentence into strings and feed it into the pattern coroutine.
    
    Arguments:
        sentence {str} -- The phrase to be splitted
        next_coroutine  -- The coroutine that the splitted sentence will be
        processed
    """
    tokens = sentence.split(" ")
    if next_coroutine is not None:
        for token in tokens:
            next_coroutine.send(token)
        next_coroutine.close()


#%% [markdown]
# Next we have the pattern_filter coroutine
#
# When this function is called, it enter in the while loop and the `(yield)`
# command "waits" for some data to be passed to him; in this mean time,
# they don't block the I/O of the program waiting for the data, it just
# continue the execution of the program. When the `coroutine.send()` is called,
# the execution of the program go back to the `yield` statement and
# runs the code bellow that.
#
# To stop the loop of the coroutine, we need to call `coroutine.stop()`;
# calling this will raise a `GeneratorExit` error.


#%%
def pattern_filter(pattern: str = 'ing', next_coroutine=None) -> None:
    """Search a pattern for a given token
    
    Keyword Arguments:
        pattern {str} -- The pattern to search in the string (default: {'ing'})
        next_coroutine -- The next coroutine in the chain (default: {None})
    
    Returns:
        None -- [description]
    """
    print(f'Searching for {pattern} pattern on the sentence')
    try:
        while True:
            token = (yield)
            if pattern in token:
                if next_coroutine is not None:
                    next_coroutine.send(token)
    except GeneratorExit:
        print('Pattern filtering coroutine ended')


#%%
def print_token(next_coroutine=None):
    try:
        while True:
            token = (yield)
            print(f'Found: {token}')
            if next_coroutine is not None:
                next_coroutine.send(token)
    except GeneratorExit:
        print('Print coroutine ended')


#%%

# Instantiating the coroutine
print_coroutine = print_token()
print_coroutine.send(None)

pattern_filter_coroutine = pattern_filter(next_coroutine=print_coroutine)
pattern_filter_coroutine.__next__()

# Creating the producer
sentence = 'Bob is running in a fast moving car'
producer(sentence, pattern_filter_coroutine)
