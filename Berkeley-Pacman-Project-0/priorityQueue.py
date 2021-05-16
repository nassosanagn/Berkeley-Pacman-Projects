#Priority Queue

import heapq

class PriorityQueue:

    def __init__(pq):
        pq.heap = []
        pq.count = 0

    def pop(pq):

        # Check if the heap is empty before popping an element
        if pq.isEmpty():
            print("The heap is empty.")
            return False
            
        pq.count -= 1
        return heapq.heappop(pq.heap)[-1]

    def push(pq, item, priority):

        # Check if item already exists in heap
        for i in range(len(pq.heap)):
            if (pq.heap[i])[1] == item:
                # If Element already exists don't push it and return False
                return False
          
        heapq.heappush(pq.heap, (priority , item))
        pq.count += 1
        return True

    def isEmpty(pq):
       return not pq.heap
    
    def update(pq,item,priority):

        i = -1
        for x in pq.heap:
            i += 1
            # x[0] is the element and x[1] is the priority
            if x[1] == item:
                if x[0] > priority:
                    pq.heap[i] = (priority , item)
                    heapq.heapify(pq.heap)
                    return True
                else:
                    # If x[0]'s priority <= new priority don't make changes
                    return False

        # If Element does not exist push it in heap
        pq.push(item, priority)
        return True


def PQSort(list):

    q = PriorityQueue()
    x = []

    for i in range(len(list)):
        q.push(list[i] , list[i])

    for i in range(len(list)):
        x.append(q.pop())
        
    return x 

