

def get_retriever(vector_store, k=5, fetch_k=10, search_type="mmr"):
    
   
      # Check for valid search_type
      if search_type not in ["mmr", "similarity"]:
          raise ValueError(f"Invalid search_type '{search_type}'. Must be 'mmr' or 'similarity'.")
      
      if search_type == "mmr":

        return vector_store.as_retriever(
        search_type=search_type,
        search_kwargs={'k': k, 'fetch_k': fetch_k}
      )
      elif search_type == "similarity":
        return vector_store.as_retriever(
           search_type=search_type,
           search_kwargs={'k': k}
       )
   
       
