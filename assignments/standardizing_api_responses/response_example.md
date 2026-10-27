## Sending Values to Response

### Kwargs

One way sending data to a response function is by using kwargs. a function call would look something like: 

```python
api_response(data=products, limit=10, offset=20)
```

which when `**kwargs` is used in the function definition, it turns all of those key-value pairs into a dictionary `{'data':products...}`. Then the easiest way to check for existing values, and set defaults if a key doesn't exist is `.get()`, especially when arguments are optional.

`**kwargs` is just a dictionary, so all the normal dictionary operations work.

### 1. Using `.get()` — preferred approach

```python

# example call
api_response(data=products, limit=10, offset=20)


def api_response(**kwargs):    
    '''
    Example use of pulling values out of kwargs and assigning defaults if keys aren't there.
    '''
    data = kwargs.get("data", [])    
    response_code = kwargs.get("response_code", 200)    
    error_response = kwargs.get("error_response", None)    
    offset = kwargs.get("offset", 0)    
    limit = kwargs.get("limit", None)    
    return {        
        "response_code": response_code,        
        "error_response": error_response,        
        "data": data,        
        "size": len(data) if isinstance(data, list) else 1,        
        "offset": offset,        
        "limit": limit,    
    }
```

### 2. Other useful approaches

| Method         | Example                    | Behavior                               |
| -------------- | -------------------------- | -------------------------------------- |
| `.get()`       | `kwargs.get("limit", 100)` | Returns default if missing             |
| Bracket access | `kwargs["limit"]`          | Raises `KeyError` if missing           |
| `.pop()`       | `kwargs.pop("limit", 100)` | Retrieves and removes the key          |
| Membership     | `"limit" in kwargs`        | Checks whether key exists              |
| Unpacking      | `func(**kwargs)`           | Passes dictionary as keyword arguments |

One subtle distinction:

```
kwargs.get("limit", 100)
```

Returns `None` if the caller explicitly passes `limit=None`. The default of `100` applies only when the key is absent.

### 3. But for your API assignment, I'd consider something better

Since you already know which parameters your response requires, explicit keyword-only arguments are arguably more Pythonic than unrestricted `**kwargs`.

```python
def api_response(
    data=None,    
    *,    
    response_code=200,    
    error_response=None,    
    total_size=None,    
    offset=None,    
    limit=None,):    
        return {        
            "response_code": response_code,        
            "error_response": error_response,        
            "data": data,        
            "total_size": total_size,        
            "size": len(data) if isinstance(data, list) else (1 if data is not None else 0),        
            "offset": offset,        
            "limit": limit,    
        }
```

Now you can call:

```
api_response(products, total_size=1000, limit=5, offset=0)
```

The `*` means that everything after it must be passed by keyword.

This has several advantages:

- IDE autocomplete knows the available arguments.
- Misspelled argument names raise errors instead of silently falling back to defaults.
- The function signature documents the API contract.
- Users can see which arguments are supported.

My recommendation: Use `.get()` when working with genuinely flexible `**kwargs`, but use explicit keyword-only parameters when the supported fields are known.

For this particular assignment, I'd favor explicit parameters. `**kwargs` is convenient, but it can also hide mistakes—and debugging a misspelled `total_szie` is nobody's idea of a good Friday night.