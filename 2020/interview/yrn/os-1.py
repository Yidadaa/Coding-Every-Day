from collections import namedtuple

def scheduler(jobs):
  named_jobs = []
  max_job_time = 0
  result = {}
  for job_name in jobs:
    arriving_time = jobs[job_name][0]
    for offset, t in jobs[job_name][1]:
      named_jobs.append([job_name, offset + arriving_time, t])
      max_job_time = max(max_job_time, named_jobs[-1][1] + named_jobs[-1][2])
    result[job_name] = [0, []] # finish time, turnaround time

  ti, ji = 0, 0
  job_queue = []

  while len(named_jobs) > 0:
    named_jobs.sort(key=lambda x: x[1])

    next_ji = ji
    max_response_job, maxi = -1, -1
    while next_ji < len(named_jobs) and named_jobs[ji][1] <= ti:
      the_job = named_jobs[next_ji]
      r = (ti - the_job[1] + the_job[2]) / the_job[2]
      if r > max_response_job:
        max_response_job = r
        maxi = next_ji
      next_ji += 1

    # compute job offset
    offset = ti - named_jobs[maxi][1]
    job_queue.append([ti, named_jobs[maxi][0]])
    ti += named_jobs[maxi][-1]

    # update job summary info
    job_name = named_jobs[maxi][0]
    result[job_name][0] = ti
    result[job_name][1].append(ti - named_jobs[maxi][1])

    # remove job from job list
    named_jobs.pop(maxi)

    # update scheduled time for each 'job_name' job
    for nji in range(len(named_jobs)):
      if named_jobs[nji][0] == job_name:
        named_jobs[nji][1] += offset

  for job_name in result:
    finish_time = result[job_name][0]
    total_ta_time = sum(result[job_name][1])
    avg_ta_time = total_ta_time / len(result[job_name][1])
    print('Job: {}\n\tFinish time: {}\n\tTurnaround time: {}\n\tAvg turnaround time: {}\n'\
      .format(job_name, finish_time, total_ta_time, avg_ta_time))

  print(job_queue)
  print(result)


jobs = {
  'A': [0, [[0, 4], [8, 4]]],
  'B': [2, [[0, 2], [6, 2]]],
  'C': [4, [[0, 6], [8, 5]]],
  'D': [6, [[0, 10]]]
}

scheduler(jobs)